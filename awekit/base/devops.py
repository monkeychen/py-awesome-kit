import os
import sys
import argparse
from datetime import datetime
from dateutil import relativedelta

from awekit import base
from awekit.base.util import datetimeutils, sshclient, compression


class DevOps(object):

    def __init__(self):
        self.args = self.parse_cli_args()

    def deploy_web_app(self, project_dir_path, remote_host="localhost", remote_port=22, user="chenzhian", password="******",
                       remote_base_dir_path="/env/demo"):
        if not os.path.exists(project_dir_path):
            print(f"The dir[{project_dir_path}] does not exist!")
            return False
        encoding = base.GBK if base.is_windows() else base.UTF_8
        project_name = os.path.basename(project_dir_path)
        os.chdir(project_dir_path)
        base.exec_shell_cmd(cmd="mvn clean package -DskipTests ", encoding=encoding)

        jar_file_name = f"perf-{project_name}-prod.jar"
        local_file_path = f"{project_dir_path}/{project_name}-backend/target/{jar_file_name}"
        remote_file_path = f"{remote_base_dir_path}/{project_name}/{jar_file_name}"
        ssh_client = sshclient.SshClient(host=remote_host, port=remote_port, user=user, password=password)
        ssh_client.upload(local_file_path=local_file_path, remote_file_path=remote_file_path)
        self.deploy_vue_frontend(project_dir_path, remote_base_dir_path, ssh_client, is_prod=True)
        self.deploy_vue_frontend(project_dir_path, remote_base_dir_path, ssh_client, is_prod=False)
        deploy_sh = f"backup-and-startup{'' if self.args.env_mode == 'prod' else '-test'}.sh"
        ssh_client.exec_command(f"{remote_base_dir_path}/{project_name}/deploy/{deploy_sh}", use_sudo=True)
        ssh_client.disconnect()

    def deploy_vue_frontend(self, project_dir_path, remote_base_dir_path, ssh_client, is_prod=True):
        encoding = base.GBK if base.is_windows() else base.UTF_8
        project_name = os.path.basename(project_dir_path)
        frontend_root_path = f"{project_dir_path}/{project_name}-frontend"
        os.chdir(frontend_root_path)
        npm_cmd = "npm run build:" + ("prod" if is_prod else "stage")
        base.exec_shell_cmd(cmd=npm_cmd, encoding=encoding)
        frontend_dist_dir_path = f"{frontend_root_path}/dist"
        zip_file_path = f"{frontend_root_path}/dist.zip"
        compression.Compression.zip_dir(frontend_dist_dir_path, zip_file_path)
        frontend_remote_file_path = f"{remote_base_dir_path}/nginx/{'prod' if is_prod else 'staging'}/dist.zip"
        ssh_client.upload(local_file_path=zip_file_path, remote_file_path=frontend_remote_file_path)
        if os.path.exists(zip_file_path):
            os.remove(zip_file_path)
        return

    def do_nothing(self):
        print(f"{base.get_timestamp(fmt=base.DEF_DATE_FMT)} => The [DevOps.do_nothing()] method was invoked ...")

    def parse_cli_args(self):
        yesterday = datetime.today() - relativedelta.relativedelta(days=1)
        def_date_id = datetimeutils.datetime_to_str(yesterday, fmt=datetimeutils.FMT_Ymd)

        cli_parser = argparse.ArgumentParser(description="DevOps辅助工具。", add_help=False)
        cli_parser.add_argument('-b', '--base_dir', nargs='?', default=f"{os.getcwd()}", help='本地项目所在目录路径。')
        cli_parser.add_argument('-d', '--date_id', nargs='?', type=int, default=def_date_id, help='日期（天），格式为yyyyMMdd，默认为昨天。')
        cli_parser.add_argument('-e', '--env_mode', nargs='?', choices=['dev', 'prod', 'test'], default='test',
                                help='设置运行环境（dev：开发环境，prod：生产环境，test：测试环境），默认为测试环境')
        cli_parser.add_argument('-f', '--func_name', nargs='?', default=f"do_nothing", help='即将调用的方法名，默认为：do_nothing')
        cli_parser.add_argument('-p', '--params', nargs='*', default=[], help='函数执行参数列表，默认为[]。')
        cli_parser.add_argument('-h', '--help', action='help', help='显示本帮助信息并退出')
        cli_parser.add_argument('-V', '--version', action='version', version='%(prog)s V0.0.1', help='显示当前版本信息并退出')
        args = cli_parser.parse_args()
        print("***" * 60)
        print(args)
        print("***" * 60)
        return args

    def execute(self):
        execute_time = datetimeutils.datetime_to_str(datetime.now(), fmt=datetimeutils.FMT_DEFAULT)
        print(f"The devops.py was executed at {execute_time}, cwd = {os.getcwd()}, sys.path={sys.path}")
        method_descr = getattr(self, self.args.func_name)
        if len(self.args.params) > 0:
            method_descr(*self.args.params)
        else:
            method_descr()
        return


if __name__ == '__main__':
    print("===" * 60)
    DevOps().execute()
    print("===" * 60)

