import argparse
import unittest


class ArgParseTest(unittest.TestCase):

    def test_fun1(self):
        parser = argparse.ArgumentParser(prog='my-program')
        parser.add_argument('-f', '--foo', help='foo of the %(prog)s program')
        parser.add_argument('--foo2', action='store_const', const=42)
        parser.add_argument('bar', nargs='?', default='123')
        parser.add_argument('--verbose', '-v', action='count', default=0)
        date_id = 20210817
        parser.add_argument('-d', '--date_id', nargs='?', type=int, default='20210817')
        parser.print_help()
        args = parser.parse_args()
        print(type(args))
        print(args)

    def test_fun2(self):
        parser = argparse.ArgumentParser(prog='my-program')
        parser.add_argument('-i', '--id', dest='tb_id_list', nargs='*', type=int, default=list(range(1, 9)), help='显式指定需要上报的数据表ID')
        # parser.add_argument('-i', '--id', nargs='*', help='显式指定需要上报的数据表ID')
        parser.print_help()
        # args = parser.parse_args()
        args = parser.parse_args("-i 1".split())
        print(args)

    def test_fun3(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--foo', nargs='*')
        parser.add_argument('bar', nargs=1)
        args = parser.parse_args('c --foo a b c d e'.split())
        print(args)



