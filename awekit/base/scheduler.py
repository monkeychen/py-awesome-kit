import os
import sys
import importlib
import yaml
from datetime import datetime
from awekit.base.util import datetimeutils
from apscheduler.schedulers.blocking import BlockingScheduler
from awekit import base
from awekit.base.security import Cryptography


class Runnable(object):

    def run(self):
        pass

    def set_scheduler(self, scheduler):
        pass


class SyncDsDescr(object):

    def __init__(self, ds_dict, sync_ds_conf: dict, kwargs: dict = None):
        ds = ds_dict[sync_ds_conf['name']]
        self.ds_dict = ds_dict
        self.sync_ds_conf = sync_ds_conf
        self.ds_type = ds['type']
        self.ds_client = ds['client']
        self.kwargs = kwargs
        self.tbname = None
        self.sql = None
        self.before = None
        self.after = None

    def prepare_stmts(self):
        period_type = self.kwargs.get('period_type')
        today_id = datetimeutils.datetime_to_str(datetime.today(), datetimeutils.FMT_Ymd)
        if period_type == 'day':
            date_id = datetimeutils.get_ago_date_id(today_id, self.kwargs.get('period_value', 1))
            self.kwargs['date_id'] = date_id
        elif period_type == 'week':
            begin_day = datetimeutils.get_ago_date_id(today_id, self.kwargs.get('period_value', 7))
            self.kwargs['begin_day'] = begin_day
            self.kwargs['end_day'] = today_id
            self.kwargs['date_id'] = datetimeutils.get_ago_date_id(today_id, 1)

        self.tbname = self.fill_params(self.sync_ds_conf.get('tbname'), valid_file=False)
        self.sql = self.fill_params(self.sync_ds_conf.get('sql'))
        self.before = self.fill_params(self.sync_ds_conf.get('before'))
        self.after = self.fill_params(self.sync_ds_conf.get('after'))

    def fill_params(self, content_or_path: str, valid_file=True):
        if content_or_path is None:
            return None
        if valid_file and os.path.exists(content_or_path):
            with open(f'{content_or_path}', 'r') as fr:
                sql = fr.read()
            content = sql.format(**self.kwargs)
        else:
            content = content_or_path.format(**self.kwargs)
        return content


class DataSyncJob(Runnable):

    def __init__(self, name, cron: str, src_ds: SyncDsDescr, dest_ds: SyncDsDescr, kwargs: dict = None):
        self.name = name
        self.cron = cron.split()
        self.src_ds = src_ds
        self.dest_ds = dest_ds
        self.kwargs = kwargs

    def run(self):
        print("===" * 60)
        print(f"Job-{self} run at {base.get_timestamp(fmt=base.DEF_DATE_FMT)} ...")
        self.src_ds.prepare_stmts()
        self.dest_ds.prepare_stmts()

        tmp_path = f"{os.getcwd()}/temp"
        src_ds_type = self.src_ds.ds_type
        if src_ds_type == 'sqlserver':
            tmp_path = f"{tmp_path}/data_sync_job_{src_ds_type}_{base.get_timestamp()}.csv"

        src_ds_client = self.src_ds.ds_client
        if self.src_ds.before is not None:
            src_ds_client.sqlcmd_stmt(self.src_ds.before)

        tmp_out_path = None
        if self.src_ds.tbname is not None:
            tmp_out_path = src_ds_client.export_table(self.src_ds.tbname, tmp_path)
        elif self.src_ds.sql is not None:
            tmp_out_path = src_ds_client.export_query(self.src_ds.sql, tmp_path)
        if tmp_out_path is None:
            print(f"{self.name} => Fail to export data from {src_ds_client}!")
            return
        if self.src_ds.after is not None:
            src_ds_client.sqlcmd_stmt(self.src_ds.after)

        dest_ds_client = self.dest_ds.ds_client
        if self.dest_ds.before is not None:
            dest_ds_client.sqlcmd_stmt(self.dest_ds.before)
        self.dest_ds.ds_client.import_table(self.dest_ds.tbname, tmp_out_path)
        if self.dest_ds.after is not None:
            dest_ds_client.sqlcmd_stmt(self.dest_ds.after)
        if os.path.exists(tmp_out_path):
            os.remove(tmp_out_path)
        print("===" * 60)
        return

    def __str__(self):
        return f"DataSyncJob[name={self.name}, cron={self.cron}, params={self.kwargs}]"


class CustomJob(Runnable):
    def __init__(self, job_conf: dict):
        self.name = job_conf['name']
        self.cron = job_conf['cron'].split()
        self.cls_path = job_conf['class']
        split_cls_path = self.cls_path.split('.')
        mod_path = ".".join(split_cls_path[0:-1])
        cls_name = split_cls_path[-1]
        module = importlib.import_module(mod_path)
        cls_descr = getattr(module, cls_name)
        self.init_method_args = job_conf['kwargs']
        if self.init_method_args is not None:
            self.cls_inst = cls_descr(**self.init_method_args)
        else:
            self.cls_inst = cls_descr()
        self.method = getattr(self.cls_inst, job_conf['method'])

    def run(self):
        print("===" * 60)
        print(f"Job-{self} run at {base.get_timestamp(fmt=base.DEF_DATE_FMT)} ...")
        self.method()
        print("===" * 60)

    def __str__(self):
        return f"CustomJob[name={self.name}, class_path={self.cls_path}, cron={self.cron}, params={self.init_method_args}]"


class JobScanner(Runnable):

    def __init__(self):
        self.scheduler = None

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler

    def scan(self):
        print(f"Scan task at {base.get_timestamp(fmt=base.DEF_DATE_FMT)} ...")
        submitted_jobs = self.scheduler.get_jobs()
        for submitted_job in submitted_jobs:
            print(f"Submitted job => {submitted_job}")


class Scheduler(object):

    def __init__(self, conf_file_path=None, base_dir_path=os.getcwd()):
        self.conf_file_path = conf_file_path
        self.crypt = Cryptography()
        if self.conf_file_path is None:
            self.conf_file_path = f"{base_dir_path}/awekit/scheduler.yml"
        self.scheduler = BlockingScheduler()
        self.ds_dict, self.jobs = self.parse_scheduler_yaml()
        self.batch_submit_job()

    def parse_scheduler_yaml(self):
        with open(self.conf_file_path) as fr:
            schedule_conf = yaml.load(fr, Loader=yaml.FullLoader)
        ds_dict = self.parse_ds_conf(dict([(ds['name'], ds) for ds in schedule_conf['datasources']]))
        jobs = self.parse_job_conf(ds_dict, schedule_conf['jobs'])
        return ds_dict, jobs

    def parse_job_conf(self, ds_dict, job_conf_list):
        jobs = []
        for job_conf in job_conf_list:
            job = None
            try:
                job_type = job_conf['type']
                if job_type == 'DataSync':
                    src_ds = SyncDsDescr(ds_dict=ds_dict, sync_ds_conf=job_conf['src_ds'], kwargs=job_conf['kwargs'])
                    dest_ds = SyncDsDescr(ds_dict=ds_dict, sync_ds_conf=job_conf['dest_ds'], kwargs=job_conf['kwargs'])
                    job = DataSyncJob(name=job_conf['name'], cron=job_conf['cron'], src_ds=src_ds, dest_ds=dest_ds, kwargs=job_conf['kwargs'])
                elif job_type == 'custom':
                    job = CustomJob(job_conf=job_conf)
            except Exception as err:
                print(f"Fail to parse job conf: {job_conf}, the error details were shown below:")
                print(str(err))
            if job is not None:
                jobs.append(job)
        return jobs

    def parse_ds_conf(self, ds_dict):
        for ds_name in ds_dict.keys():
            ds = ds_dict[ds_name]
            ds['encrypt_pwd'] = ds['password']
            ds['password'] = self.crypt.decrypt(ds['encrypt_pwd'])
            split_cls_path = ds['class'].split('.')
            mod_path = ".".join(split_cls_path[0:-1])
            cls_name = split_cls_path[-1]
            module = importlib.import_module(mod_path)
            cls_descr = getattr(module, cls_name)
            if ds['type'] == 'oracle':
                ds['client'] = cls_descr(tns_name=ds['tns_name'], user=ds['user'], password=ds['password'])
            else:
                ds['client'] = cls_descr(host=ds['host'], port=ds['port'], dbname=ds['dbname'], user=ds['user'], password=ds['password'])
        return ds_dict

    def batch_submit_job(self):
        for job in self.jobs:
            if job.__class__.__name__ == "CustomJob" and job.cls_inst.__class__.__name__ == "JobScanner":
                getattr(job.cls_inst, "set_scheduler")(self.scheduler)
            self.scheduler.add_job(job.run, 'cron', second=job.cron[0], minute=job.cron[1], hour=job.cron[2], day=job.cron[3],
                                   month=job.cron[4], day_of_week=job.cron[5], id=job.name, name=job.name)
            print(f"Success to submit job[{job}] at {base.get_timestamp()}!")

    def startup(self):
        self.scheduler.start()


if __name__ == "__main__":
    print("===" * 60)
    print(f"Startup lighter configurable scheduler at {datetimeutils.datetime_to_str(datetime.now())} ...")
    print("~~~" * 60)
    print(f"sys.path = {sys.path}")
    print("~~~" * 60)
    scheduler = Scheduler()
    scheduler.startup()
