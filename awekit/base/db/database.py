import os
import subprocess
import time
from awekit import base


class Database(object):
    USER_HOME = os.getenv("USERPROFILE") if base.is_windows() else os.getenv("HOME")
    USER_NAME = os.getenv("USERNAME") if base.is_windows() else os.getenv("USER")
    CMD_QUOTA = "\"" if base.is_windows() else "'"
    LOG_HOME = f"{USER_HOME}/logs"
    COL_SEPARATOR = "|"

    def __init__(self, extra_params: dict = None):
        self.extra_params = extra_params
        self.change_common_params(extra_params)

    def change_common_params(self, params: dict = None):
        if params is not None:
            self.USER_HOME = params["user_home"] if "user_home" in params else (os.getenv("USERPROFILE") if base.is_windows() else os.getenv("HOME"))
            self.USER_NAME = params["user_name"] if "user_name" in params else (os.getenv("USERNAME") if base.is_windows() else os.getenv("USER"))
            self.CMD_QUOTA = params["cmd_quota"] if "cmd_quota" in params else ("\"" if base.is_windows() else "'")
            self.LOG_HOME = params["log_home"] if "log_home" in params else f"{self.USER_HOME}/logs"

        if not os.path.exists(self.LOG_HOME):
            os.mkdir(self.LOG_HOME)

    def show_params(self):
        print("===" * 50)
        print(f"USER_HOME = {self.USER_HOME}, USER_NAME = {self.USER_NAME}, LOG_HOME = {self.LOG_HOME}, extra_params = {self.extra_params}")
        print("===" * 50)

    def show_conn_info(self):
        pass

    def wrap_param(self, param):
        return self.CMD_QUOTA + param + self.CMD_QUOTA

    def get_bin_dir(self):
        bin_dir_path = self.USER_HOME + "/bin"
        if (self.extra_params is not None) and ("bin_dir_path" in self.extra_params):
            bin_dir_path = self.extra_params["bin_dir_path"]
        return bin_dir_path

    def execute_cmd(self, cmd, dt_flag=None, encoding=base.UTF_8):
        b_t = time.time()
        cmd_id = dt_flag
        if cmd_id is None:
            cmd_id = self.get_timestamp()
        print(f"cmd[id = {cmd_id}] => {cmd}")
        exec_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result_str = str(exec_result.stdout, encoding=encoding).strip()
        e_t = time.time()
        print(f"Shell script[cmd_id = {cmd_id}, cost_time = {round(e_t - b_t, 2)}s]'s execution result is: \n{result_str}")
        return result_str, result_str.lower().find("error") == -1

    def sqlcmd_stmt(self, stmt, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=COL_SEPARATOR):
        pass

    def sqlcmd_file(self, sql_file_path, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=COL_SEPARATOR):
        pass

    def sqlcmd(self, stmt_or_file: str, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=COL_SEPARATOR, is_stmt=True):
        pass

    def get_timestamp(self):
        return base.get_timestamp()
