import argparse
import os
from datetime import datetime

from dateutil import relativedelta

from awekit.base.util import datetimeutils


class CliHelper(object):

    def parse_cli_args_template(self):
        scheduled_time = datetimeutils.datetime_to_str(datetime.now(), fmt=datetimeutils.FMT_DEFAULT)
        yesterday = datetime.today() - relativedelta.relativedelta(days=1)
        def_date_id = datetimeutils.datetime_to_str(yesterday, fmt=datetimeutils.FMT_Ymd)

        cli_parser = argparse.ArgumentParser(description="这是一个用于将业务数据上报给北向数据平台的工具。", add_help=False)
        cli_parser.add_argument('-d', '--date_id', nargs='?', type=int, default=def_date_id, help='上报日期（天），格式为yyyyMMdd，默认为昨天。')
        cli_parser.add_argument('-e', '--env_mode', nargs='?', choices=['dev', 'prod', 'patch'], default='test',
                                help='设置运行环境（dev：开发环境，prod：生产环境，test：测试环境-补数据），默认为生产环境')
        cli_parser.add_argument('-r', '--remote_ftp_dir', nargs='*', default=["/dir1", "/dir2"], help='省内FTP服务器目录，默认为["/dir1", "/dir2"]。')
        cli_parser.add_argument('-s', '--per_file_size', nargs='?', type=int, default=100, help='按行分割，使分割后的每个文件尽量达到指定大小（单位MB），默认100MB。')
        cli_parser.add_argument('-i', '--tb_id', nargs='*', type=int, default=list(range(1, 100)), help='显式指定需要上报的数据表ID列表，默认上报所有已配置的数据表')
        cli_parser.add_argument('-w', '--workspace_dir', nargs='?', default=f"{os.getcwd()}/workspace", help='工作空间所在目录路径，默认为当前目录。')
        cli_parser.add_argument('-h', '--help', action='help', help='显示本帮助信息并退出')
        cli_parser.add_argument('-V', '--version', action='version', version='%(prog)s V0.0.1', help='显示当前版本信息并退出')
        args = cli_parser.parse_args()
        print(f"The programme[{cli_parser.prog}] was scheduled at {scheduled_time}, cwd = {os.getcwd()}, env_mode = {args.env_mode}, "
              f"workspace = {args.workspace_dir}, date_id = {args.date_id}")
        return args


if __name__ == "__main__":
    CliHelper().parse_cli_args_template()
