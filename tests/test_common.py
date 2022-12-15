import os
import platform
import csv
from datetime import *
import unittest
import magic_pylib
import awekit
from awekit.base.util import datetimeutils


class CommonTest(unittest.TestCase):

    def test_datetimeutils(self):
        print(datetimeutils.datetime_to_str(datetime.now(), datetimeutils.FMT_DEFAULT))
        print(datetime.now().timestamp() * 1000)

    def test_magic_pylib(self):
        print(magic_pylib.get_resource_absolute_path("resources/config.yml"))
        print(magic_pylib.get_resource_data("resources/config.yml"))

    def test_awesome(self):
        print(awekit.get_resource_absolute_path("base/resources/config.yml"))
        print(awekit.get_resource_data("base/resources/config.yml"))

    def test_str_encoding(self):
        str1 = "人人"
        byte1 = str1.encode("GBK")  # 采用GBK编码进行转换
        byte2 = str1.encode("utf-8")  # 采用utf-8编码进行转换
        print("原字符串：", str1)
        print("GBK转换：", byte1)
        print("utf-8转换：", byte2)
        print("GBK还原：", byte1.decode(encoding="GBK"))
        print("utf-8还原1：", byte2.decode())
        print("utf-8还原2：", byte2.decode(encoding="utf-8"))

    def test_file_open(self):
        test_dir_path = os.getcwd() if platform.system() in ("Linux", "Darwin") else os.getcwd() + "/temp"
        fp = test_dir_path + '/csvfile.csv'
        csvfile = open(fp, 'w', newline=None)
        # writer = csv.writer(csvfile, lineterminator='\n')
        writer = csv.writer(csvfile)
        writer.writerow('a')
        writer.writerow('b')
        csvfile.close()
        csvfile = open(fp, 'r', newline=None)
        txtdata = csvfile.read()
        print(txtdata)
        csvfile.close()
        tf = open(test_dir_path + '/csvfile2.csv', 'w', newline='')
        tf.write(txtdata)
        tf.close()


if __name__ == '__main__':
    unittest.main()
