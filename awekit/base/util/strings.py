import sys
import os
import hashlib
from awekit import base


def clear_null_char(input_str: str, encoding=base.UTF_8):
    return input_str.replace(b'\x00'.decode(encoding=encoding), "")


def clear_null_char_in_file(input_file, encoding=base.UTF_8):
    tmp_path = f"{input_file}.tmp"
    file_writer = open(tmp_path, "w", encoding=encoding)
    lines = []
    with open(input_file, "r", encoding=encoding) as file_reader:
        for line in file_reader.readlines():
            line = clear_null_char(line, encoding=encoding)
            lines.append(line)
            if len(lines) == 100:
                file_writer.writelines(lines)
                lines.clear()

        file_writer.writelines(lines)
    file_writer.close()
    os.remove(input_file)
    os.rename(tmp_path, input_file)


def show_python_version():
    print("Python Version ====>>>>" + sys.version)


def md5(msg):
    return hashlib.md5(msg.encode(encoding=base.UTF_8)).hexdigest()


if __name__ == '__main__':
    show_python_version()
