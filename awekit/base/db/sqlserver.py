import os
from awekit import base
from awekit.base.db.database import Database


class SqlServer(Database):

    def __init__(self, host: str, port: int = 1433, dbname: str = None, user: str = None,
                 password: str = None, extra_params: dict = None):
        super().__init__(extra_params=extra_params)
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connect_info = f"-S {self.host},{self.port} -U {self.user} -P '{self.password}' -d {self.dbname}"
        if base.is_windows():
            self.connect_info = f"-S {self.host},{self.port} -U {self.user} -P \"{self.password}\" -d {self.dbname}"

    def show_conn_info(self):
        print(self.connect_info)

    def get_bin_dir(self):
        bin_dir_path = "C:/mssql-tools/bin" if base.is_windows() else "/opt/mssql-tools/bin"
        if (self.extra_params is not None) and ("bin_dir_path" in self.extra_params):
            bin_dir_path = self.extra_params["bin_dir_path"]
        return bin_dir_path

    def sqlcmd_stmt(self, stmt, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        return self.sqlcmd(stmt, out_file_path=out_file_path, show_header=show_header, encoding=encoding, delimiter=delimiter, is_stmt=True)

    def sqlcmd_file(self, sql_file_path, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        return self.sqlcmd(sql_file_path, out_file_path=out_file_path, show_header=show_header, encoding=encoding, delimiter=delimiter, is_stmt=False)

    def sqlcmd(self, stmt_or_file: str, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR, is_stmt=True):
        if stmt_or_file is None:
            print("The argument[stmt_or_file] MUST NOT be None!!!")
            return -1

        cmd_content = f" -Q \"{stmt_or_file}\" " if is_stmt else f" -i {self.wrap_param(stmt_or_file)} "

        delimiter = self.wrap_param(delimiter)
        output_options = f" -W -s {delimiter} "
        if out_file_path is not None:
            output_options = output_options + f" -o {self.wrap_param(out_file_path)} "

        mssql_cmd = f"{self.get_bin_dir()}/sqlcmd {self.connect_info} {cmd_content} {output_options}"
        return self.execute_cmd(mssql_cmd, encoding=encoding)

    def import_table(self, tb_name, in_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        delimiter = self.wrap_param(delimiter)
        mssql_cmd = f"{self.get_bin_dir()}/bcp {tb_name} in {in_file_path} {self.connect_info} -c -t {delimiter} "
        self.execute_cmd(mssql_cmd, encoding=encoding)
        return True

    def export_table(self, tb_name, out_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        delimiter = self.wrap_param(delimiter)
        mssql_cmd = f"{self.get_bin_dir()}/bcp {tb_name} out {out_file_path} {self.connect_info} -c -t {delimiter} "
        self.execute_cmd(mssql_cmd, encoding=encoding)
        return out_file_path

    def export_query(self, stmt, out_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        delimiter = self.wrap_param(delimiter)
        mssql_cmd = f"{self.get_bin_dir()}/bcp \"{stmt}\" queryout {out_file_path} {self.connect_info} -c -t {delimiter} "
        self.execute_cmd(mssql_cmd, encoding=encoding)
        return out_file_path


if __name__ == "__main__":
    print(os.getcwd())
