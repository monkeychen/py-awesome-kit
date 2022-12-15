import os
from awekit import base
from awekit.base.db.database import Database


class Oracle(Database):

    def __init__(self, tns_name: str, user: str = "sa", password: str = None, extra_params: dict = None):
        super().__init__(extra_params=extra_params)
        self.tns_name = tns_name
        self.user = user
        self.password = password
        self.connect_info = f"user={self.user}/{self.password}@{self.tns_name} "

    def show_conn_info(self):
        print(self.connect_info)

    def get_bin_dir(self):
        bin_dir_path = "/env/oracle/instantclient_21_3"
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

        cmd_content = f" query=\"{stmt_or_file}\" " if is_stmt else f" sql={self.wrap_param(stmt_or_file)} "

        delimiter = self.wrap_param(delimiter)
        output_options = (" head=Yes " if show_header else " head=No ") + f" text=CSV field={delimiter} charset={encoding} "

        if out_file_path is None:
            out_file_path = f"{os.getcwd()}/temp/sqluldr_out_{base.get_timestamp()}.csv"
        output_options = output_options + f" file={self.wrap_param(out_file_path)} "

        mssql_cmd = f"{self.get_bin_dir()}/sqluldr2 {self.connect_info} {cmd_content} {output_options}"
        return self.execute_cmd(mssql_cmd, encoding=encoding)

    def import_table(self, tb_name, in_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        raise Exception("Not support yet!!!")

    def export_table(self, tb_name, out_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR, where_clause=" 1 = 1 "):
        stmt = f"select * from {tb_name} where {where_clause}"
        self.sqlcmd_stmt(stmt, out_file_path=out_file_path, show_header=False, encoding=encoding, delimiter=delimiter)
        return out_file_path

    def export_query(self, stmt, out_file_path, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        self.sqlcmd_stmt(stmt, out_file_path=out_file_path, show_header=False, encoding=encoding, delimiter=delimiter)
        return out_file_path


if __name__ == "__main__":
    print(os.getcwd())
