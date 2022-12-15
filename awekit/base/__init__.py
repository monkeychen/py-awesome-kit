import os
import platform
import subprocess
import time
from datetime import datetime

UTF_8 = "UTF-8"
UTF8 = "UTF8"
GBK = "GBK"
DEF_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def is_windows():
    return platform.system() not in ("Linux", "Darwin")


def is_linux():
    return platform.system() == "Linux"


def is_macos():
    return platform.system() == "Darwin"


def get_timestamp(fmt="%Y%m%d%H%M%S"):
    return datetime.now().strftime(fmt)


def method_time_elapsed(method):
    def wrapper(self, *args, **kwargs):
        b_t = time.time()
        res = method(self, *args, **kwargs)
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to invoke this [{method.__name__}] method!")
        return res
    return wrapper


def func_time_elapsed(func):
    def wrapper(*args, **kwargs):
        b_t = time.time()
        res = func(*args, **kwargs)
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to invoke this [{func.__name__}] method!")
        return res
    return wrapper


def exec_shell_cmd(cmd, dt_flag=None, encoding=UTF_8):
    b_t = time.time()
    cmd_id = dt_flag
    if cmd_id is None:
        cmd_id = get_timestamp()
    print(f"cmd[id = {cmd_id}] => {cmd}")
    exec_result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result_str = str(exec_result.stdout, encoding=encoding).strip()
    e_t = time.time()
    print(f"Shell script[cmd_id = {cmd_id}, cost_time = {round(e_t - b_t, 2)}s]'s execution result is: \n{result_str}")
    return result_str, result_str.lower().find("error") == -1


def make_parent_dirs(file_path: str):
    dir_path = os.path.dirname(file_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


