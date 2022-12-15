import sys

from awekit import base
from awekit.base.db.database import Database
from awekit.base.util.sshclient import SshClient


class Greenplum(Database):

    def __init__(self, host=None, port=5432, dbname=None, user=None,
                 password=None, extra_params: dict = None):
        super().__init__(extra_params=extra_params)
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connect_info = f"'dbname={self.dbname} host={self.host} port={self.port} user={self.user} password={self.password}'"
        if base.is_windows():
            self.connect_info = f"\"dbname={self.dbname} host={self.host} port={self.port} user={self.user} password='{self.password}'\""

    def show_conn_info(self):
        print(self.connect_info)

    def get_client_bin_dir(self):
        bin_dir_path = "/env/greenplum/clients/bin"
        if (self.extra_params is not None) and ("client_bin_dir_path" in self.extra_params):
            bin_dir_path = self.extra_params["client_bin_dir_path"]
        return bin_dir_path

    def get_bin_dir(self):
        return self.get_client_bin_dir()

    def get_loader_bin_dir(self):
        bin_dir_path = "/env/greenplum/loaders/bin"
        if (self.extra_params is not None) and ("loader_bin_dir_path" in self.extra_params):
            bin_dir_path = self.extra_params["loader_bin_dir_path"]
        return bin_dir_path

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

        sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} {cmd_content} {output_options} "
        if base.is_windows():
            sql_cmd = f"{self.get_client_bin_dir()}/psql {cmd_content} {output_options} {self.connect_info} "
        return self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)

    def import_table(self, tb_name, local_csv_file_path, schema=None, where_clause=" 1 = 1 ",
                     gpfdist_url=None, gpfdist_dir_path=None,
                     jump_host=None, jump_port=22, jump_user=None, jump_pwd=None,
                     encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        dt_flag = self.get_timestamp()
        ext_tb_name = f"{tb_name}_{dt_flag}_in_ext"
        csv_file_name = f"{tb_name}_{dt_flag}.csv"

        upload_success = True
        remote_file_path = f"{gpfdist_dir_path}/{csv_file_name}"
        ssh_client = None
        try:
            ssh_client = SshClient(host=jump_host, port=jump_port, user=jump_user, password=jump_pwd)
            ssh_client.upload(local_csv_file_path, remote_file_path)
        except Exception as e:
            print(f"Fail to upload local file from [{local_csv_file_path}] to jumper-host[host = {jump_host}, remote-path = {remote_file_path}]!")
            print(str(e))
            upload_success = False
        finally:
            if ssh_client is not None:
                ssh_client.disconnect()
        try:
            main_sql = f'''
                    drop external table if exists {schema}.{ext_tb_name};
                    create external table {schema}.{ext_tb_name} (like {schema}.{tb_name})
                    LOCATION ('{gpfdist_url}/{csv_file_name}') FORMAT 'csv' (DELIMITER '{delimiter}' null '');
                    insert into {schema}.{tb_name} select * from {schema}.{ext_tb_name} where {where_clause};
                    '''
            sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} -c \"{main_sql}\" "
            if base.is_windows():
                sql_cmd = f"{self.get_client_bin_dir()}/psql -c \"{main_sql}\" {self.connect_info} "
            self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)

            drop_tb_sql = f"drop external table if exists {schema}.{ext_tb_name}"
            sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} -c \"{drop_tb_sql}\" "
            if base.is_windows():
                sql_cmd = f"{self.get_client_bin_dir()}/psql -c \"{drop_tb_sql}\" {self.connect_info} "
            self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)
        except Exception as e:
            print(f"Fail to import data to greenplum db's table[{tb_name}] from local file[{local_csv_file_path}], the error is {e}!")
            upload_success = False
        return upload_success

    def export_table(self, tb_name: str, local_out_dir_path: str, schema=None, where_clause=" 1 = 1 ",
                     gpfdist_url=None, gpfdist_dir_path=None,
                     jump_host=None, jump_port=22, jump_user=None, jump_pwd=None,
                     encoding=base.UTF_8, delimiter=Database.COL_SEPARATOR):
        dt_flag = self.get_timestamp()
        ext_tb_name = f"{tb_name}_{dt_flag}_out_ext"
        csv_file_name = f"{tb_name}_{dt_flag}.csv"
        main_sql = f'''
        drop external table if exists {schema}.{ext_tb_name};
        create writable external table {schema}.{ext_tb_name} (like {schema}.{tb_name})
        LOCATION ('{gpfdist_url}/{csv_file_name}') FORMAT 'csv' (DELIMITER '{delimiter}' null '');
        insert into {schema}.{ext_tb_name} select * from {schema}.{tb_name} where {where_clause};
        '''
        sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} -c \"{main_sql}\" "
        if base.is_windows():
            sql_cmd = f"{self.get_client_bin_dir()}/psql -c \"{main_sql}\" {self.connect_info} "
        self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)

        local_file_path = f"{local_out_dir_path}/{csv_file_name}"
        remote_file_path = f"{gpfdist_dir_path}/{csv_file_name}"
        ssh_client = None
        try:
            ssh_client = SshClient(host=jump_host, port=jump_port, user=jump_user, password=jump_pwd)
            ssh_client.download(local_file_path, remote_file_path)
            ssh_client.exec_command(f"rm -f {remote_file_path}")
        except Exception as e:
            print("Fail to ssh to jumper host and download target file")
            print(str(e))
        finally:
            if ssh_client is not None:
                ssh_client.disconnect()

        drop_tb_sql = f"drop external table if exists {schema}.{ext_tb_name}"
        sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} -c \"{drop_tb_sql}\" "
        if base.is_windows():
            sql_cmd = f"{self.get_client_bin_dir()}/psql -c \"{drop_tb_sql}\" {self.connect_info} "
        self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)
        return local_file_path

    def export_query(self, export_sql: str, local_file_path: str, remote_file_path: str,
                     jump_host=None, jump_port=22, jump_user=None, jump_pwd=None, encoding=base.UTF_8):
        dt_flag = self.get_timestamp()
        sql_cmd = f"{self.get_client_bin_dir()}/psql {self.connect_info} -c \"{export_sql}\" "
        if base.is_windows():
            sql_cmd = f"{self.get_client_bin_dir()}/psql -c \"{export_sql}\" {self.connect_info} "
        self.execute_cmd(sql_cmd, dt_flag=dt_flag, encoding=encoding)
        ssh_client = None
        try:
            ssh_client = SshClient(host=jump_host, port=jump_port, user=jump_user, password=jump_pwd)
            ssh_client.download(local_file_path, remote_file_path)
            ssh_client.exec_command(f"rm -f {remote_file_path}")
        except Exception as e:
            print("Fail to ssh to jumper host and download target file")
            print(str(e))
        finally:
            if ssh_client is not None:
                ssh_client.disconnect()
        return local_file_path


if __name__ == "__main__":
    gp = Greenplum(host="localhost")
    gp.show_conn_info()
    gp.export_table(sys.argv[1], sys.argv[2], where_clause=sys.argv[3], delimiter="|")
