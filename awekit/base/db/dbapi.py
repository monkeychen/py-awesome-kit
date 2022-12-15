import pymssql
import pymysql
import pymysql.cursors
import dmPython as dmPy
from awekit import base
from awekit.base import logger_factory


class MsSql(object):

    def __init__(self, host: str, port: int = 1433, dbname: str = None, user: str = "sa", password: str = None,
                 charset: str = None, auto_commit: bool = True, auto_connect: bool = True, log_path: str = None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        if charset is None:
            charset = base.GBK if base.is_windows() else base.UTF_8
        self.charset = charset
        self.auto_commit = auto_commit
        self.session: pymssql.Connection = None
        if auto_connect:
            self.session = self.connect()
        if log_path is not None:
            self.logger = logger_factory.new_logger("dbapi-mssql-logger", log_file_path=log_path, stdout_enable=False)
        else:
            self.logger = logger_factory.new_logger("dbapi-mssql-logger")

    def connect(self) -> pymssql.Connection:
        session: pymssql.Connection = pymssql.connect(server=self.host, port=self.port, database=self.dbname,
                                                      user=self.user, password=self.password, charset=self.charset)
        if session is not None:
            session.autocommit(self.auto_commit)
        return session

    def cursor(self, as_dict: bool = False) -> pymssql.Cursor:
        if self.session is None:
            self.session = self.connect()
        return self.session.cursor(as_dict)

    def execute(self, stmt, params: tuple, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            cursor.execute(stmt, params)
            if callback is not None:
                callback(cursor, self.logger)

    def executemany(self, stmt, params: list, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            cursor.executemany(stmt, params)
            if callback is not None:
                callback(cursor, self.logger)

    def close(self):
        if self.session is not None:
            self.session.close()


class MySql(object):

    def __init__(self, host: str, port: int = 3306, dbname: str = None, user: str = "root", password: str = None,
                 charset: str = None, auto_commit: bool = True, auto_connect: bool = True, log_path: str = None):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        if charset is None:
            charset = base.GBK if base.is_windows() else base.UTF8
        self.charset = charset
        self.auto_commit = auto_commit
        self.session: pymysql.Connection = None
        if auto_connect:
            self.session = self.connect()
        if log_path is not None:
            base.make_parent_dirs(log_path)
            self.logger = logger_factory.new_logger("dbapi-mysql-logger", log_file_path=log_path, stdout_enable=False)
        else:
            self.logger = logger_factory.new_logger("dbapi-mysql-logger")

    def connect(self) -> pymysql.Connection:
        session: pymysql.Connection = pymysql.connect(host=self.host, port=self.port, database=self.dbname,
                                                      user=self.user, password=self.password, charset=self.charset)
        if session is not None:
            session.autocommit(self.auto_commit)
        return session

    def cursor(self, as_dict: bool = False) -> pymysql.cursors.Cursor:
        if self.session is None:
            self.session = self.connect()
        if as_dict:
            return self.session.cursor(cursor=pymysql.cursors.DictCursor)
        return self.session.cursor()

    def execute(self, stmt, params: tuple = None, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            affect_rows = cursor.execute(stmt, params)
            if callback is not None:
                callback(cursor, affect_rows, self.logger)
        return affect_rows

    def executemany(self, stmt, params: list, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            affect_rows = cursor.executemany(stmt, params)
            if callback is not None:
                callback(cursor, affect_rows, self.logger)
        return affect_rows

    def close(self):
        if self.session is not None:
            self.session.close()


class DmSql(object):

    def __init__(self, host: str, port: int = 5236, user: str = "SYSDBA", password: str = 'SYSDBA',
                 charset=None, auto_commit: bool = True, auto_connect: bool = True, log_path: str = None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.schema = user
        if charset is None:
            charset = dmPy.PG_GBK if base.is_windows() else dmPy.PG_UTF8
        self.charset = charset
        self.auto_commit = auto_commit
        self.session: dmPy.Connection = None
        if auto_connect:
            self.session = self.connect()
        if log_path is not None:
            self.logger = logger_factory.new_logger("dbapi-dm-logger", log_file_path=log_path, stdout_enable=False)
        else:
            self.logger = logger_factory.new_logger("dbapi-dm-logger")

    def connect(self) -> dmPy.Connection:
        return dmPy.connect(server=self.host, port=self.port, user=self.user, password=self.password,
                            local_code=self.charset, autoCommit=self.auto_commit)

    def cursor(self) -> dmPy.Cursor:
        if self.session is None:
            self.session = self.connect()
        return self.session.cursor()

    def execute(self, stmt, params: tuple = None, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            cursor.execute(stmt, params)
            if callback is not None:
                callback(cursor, self.logger)

    def executemany(self, stmt, params: list = None, callback=None):
        with self.cursor() as cursor:
            self.logger.info(f"SQL: {stmt}, PARAMS: {params}")
            cursor.executemany(stmt, params)
            if callback is not None:
                callback(cursor, self.logger)

    def close(self):
        if self.session is not None:
            self.session.close()
