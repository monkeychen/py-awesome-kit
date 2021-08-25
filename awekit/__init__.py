from pkg_resources import resource_filename, resource_string

CHARSET_UTF_8 = "UTF-8"
CHARSET_GBK = "GBK"


def get_resource_absolute_path(res_relative_path):
    return resource_filename(__name__, res_relative_path)


def get_resource_data(res_relative_path, encoding="UTF-8"):
    return str(resource_string(__name__, res_relative_path), encoding)