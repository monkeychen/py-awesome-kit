import os

from awekit import base
from awekit.base.db.database import Database


class Aster(Database):

    def __init__(self, host, user, password, dbname="beehive", port=2406, loader_host="localhost", extra_params: dict = None, check_os=True):
        super().__init__(extra_params=extra_params)
        if check_os and base.is_windows():
            raise Exception("Not support Windows platform!")
        self.host = host
        self.loader_host = loader_host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connect_info = f" -h {self.host} -p {self.port} -d {self.dbname} -U {self.user} -w {self.password} "

    def show_conn_info(self):
        print(self.connect_info)

    def get_client_bin_dir(self):
        bin_dir_path = "/env/aster/bin"
        if (self.extra_params is not None) and ("client_bin_dir_path" in self.extra_params):
            bin_dir_path = self.extra_params["client_bin_dir_path"]
        return bin_dir_path

    def get_bin_dir(self):
        return self.get_client_bin_dir()

    def sqlcmd_stmt(self, stmt, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        return self.sqlcmd(stmt, out_file_path=out_file_path, show_header=show_header, encoding=encoding, delimiter=delimiter, is_stmt=True)

    def sqlcmd_file(self, sql_file_path, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        return self.sqlcmd(sql_file_path, out_file_path=out_file_path, show_header=show_header, encoding=encoding, delimiter=delimiter, is_stmt=False)

    def sqlcmd(self, stmt_or_file: str, out_file_path=None, show_header=True, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR, is_stmt=True):
        if stmt_or_file is None:
            print("The argument[stmt_or_file] MUST NOT be None!!!")
            return -1

        cmd_content = f" -c \"{stmt_or_file}\" " if is_stmt else f" -f {stmt_or_file} "

        dt_flag = self.get_timestamp()
        delimiter = self.wrap_param(delimiter)
        output_options = (" " if show_header else " -t ") + f" -A -F {delimiter} "
        if out_file_path is not None:
            output_options = output_options + " -o " + out_file_path

        sql_cmd = f"{self.get_client_bin_dir()}/act {self.connect_info} {cmd_content} {output_options} "
        return self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)

    def import_table(self, tb_name: str, local_csv_file_path: str, schema: str, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        import_success = True
        try:
            sql_cmd = f"{self.get_client_bin_dir()}/ncluster_loader {self.connect_info} -f -l {self.loader_host} -c " \
                      f" -D '{delimiter}' -n '' {schema}.{tb_name} {local_csv_file_path}"
            self.execute_cmd(sql_cmd, encoding=encoding)
        except Exception as e:
            print(f"Fail to import data to Aster's table[{tb_name}] from local file[{local_csv_file_path}], the error is {e}!")
            import_success = False
        return import_success

    def export_table(self, tb_name: str, local_out_dir_path: str, schema: str, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        dt_flag = self.get_timestamp()
        csv_file_name = f"{tb_name}_{dt_flag}.csv"
        if not os.path.exists(local_out_dir_path):
            os.makedirs(local_out_dir_path)
        local_file_path = f"{local_out_dir_path}/{csv_file_name}"
        sql_cmd = f"{self.get_client_bin_dir()}/ncluster_export {self.connect_info} -f -l {self.loader_host} -c " \
                  f" -D '{delimiter}' -n '' {schema}.{tb_name} {local_file_path}"
        self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)
        return local_file_path

    def export_query(self, export_sql: str, local_out_dir_path: str, schema: str, encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        dt_flag = self.get_timestamp()
        tmp_tb_name = f"f_{self.USER_NAME}_tmp_tb_for_export_{dt_flag}"
        tmp_sql = f"create fact table {schema}.{tmp_tb_name} as {export_sql}"
        sql_cmd = f"{self.get_client_bin_dir()}/act {self.connect_info} -c \"{tmp_sql}\" "
        local_file_path = None
        try:
            self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)
            local_file_path = self.export_table(tb_name=tmp_tb_name, local_out_dir_path=local_out_dir_path, schema=schema, encoding=encoding, delimiter=delimiter)
        except Exception as e:
            print(f"Fail to export data from query[{export_sql}], the error is {e}!")
        finally:
            drop_sql = f"drop table if exists {schema}.{tmp_tb_name}"
            sql_cmd = f"{self.get_client_bin_dir()}/act {self.connect_info} -c \"{drop_sql}\" "
            self.execute_cmd(sql_cmd, encoding=encoding)
        return local_file_path

    def add_partition(self, tb_name, date_id, schema: str):
        add_sql = f"alter table {schema}.{tb_name} add partition p{date_id} (values({date_id}))"
        self.sqlcmd(add_sql)

    def drop_partition(self, tb_name, date_id, schema: str):
        drop_sql = f"alter table {schema}.{tb_name} drop partition (p{date_id})"
        self.sqlcmd(drop_sql)


if __name__ == "__main__":
    aster = Aster(host="localhost", user="user", password="******")
    aster.show_conn_info()
