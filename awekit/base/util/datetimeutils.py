import time
import datetime

FMT_DEFAULT = "%Y-%m-%d %H:%M:%S"
FMT_Ymd = "%Y%m%d"
FMT_YmdHMS = "%Y%m%d%H%M%S"
FMT_HMS = "%H%M%S"


def str_to_time(time_str, fmt=FMT_DEFAULT):
    return time.strptime(time_str, fmt)


def str_to_datetime(dt_str, fmt=FMT_DEFAULT):
    return datetime.datetime.strptime(dt_str, fmt)


def time_to_str(tm, fmt=FMT_DEFAULT):
    return tm.strftime(fmt)


def datetime_to_str(dt, fmt=FMT_DEFAULT):
    return dt.strftime(fmt)


def time_to_timestamp(tm):
    return time.mktime(tm)


def timestamp_to_time(ts):
    return time.localtime(ts)


def datetime_to_timestamp(dt):
    return dt.timestamp()


def timestamp_to_datetime(ts):
    return datetime.datetime.fromtimestamp(ts)


def datetime_to_time(dt):
    return dt.timetuple()


def time_to_datetime(tm):
    return datetime.datetime(*tm[0:6])


def timestamp_to_str(ts, fmt=FMT_DEFAULT):
    return datetime_to_str(timestamp_to_datetime(ts), fmt)

