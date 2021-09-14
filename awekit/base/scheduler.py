import os
import importlib
import yaml
from dateutil import relativedelta
from apscheduler.schedulers.blocking import BlockingScheduler

from awekit import base
from awekit.base.security import Cryptography


class Task(object):

    def run(self):
        print(f"I'm the {self.__class__.__name__}")


class TaskScanner(object):

    def __init__(self, scheduler):
        self.scheduler = scheduler

    def scan(self):
        print(f"Scan task at {base.get_timestamp()} ...")


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

        ds_dict = dict([(ds['name'], ds) for ds in schedule_conf['datasources']])
        self.parse_ds_conf(ds_dict)
        jobs = schedule_conf['jobs']
        for job in jobs:
            pass
        return ds_dict, jobs

    def parse_ds_conf(self, ds_dict):
        for ds_name in ds_dict.keys():
            ds = ds_dict[ds_name]
            ds['encrypt_pwd'] = ds['password']
            ds['password'] = self.crypt.decrypt(ds['encrypt_pwd'])
            split_mod_path = ds['class'].split('.')
            mod_path = ".".join(split_mod_path[0:-1])
            cls_name = split_mod_path[-1]
            module = importlib.import_module(mod_path)
            cls_inst = getattr(module, cls_name)
            if ds['type'] == 'oracle':
                ds['client'] = cls_inst(tns_name=ds['tns_name'], user=ds['user'], password=ds['password'])
            else:
                ds['client'] = cls_inst(host=ds['host'], port=ds['port'], dbname=ds['dbname'], user=ds['user'], password=ds['password'])
        return ds_dict

    def batch_submit_job(self):
        pass

    def startup(self):
        self.scheduler.start()


if __name__ == "__main__":
    scheduler = Scheduler()
