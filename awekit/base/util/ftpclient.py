import ftplib


class FtpClient:
    def __init__(self, host, username, password, port=21, auto_connect=True):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.ftp = ftplib.FTP()
        if auto_connect:
            print(f"Start to connect to ftp server : {host}")
            self.connect()

    def connect(self):
        # 打开调试级别2，显示详细信息
        # ftp.set_debuglevel(2)
        self.ftp.connect(self.host, self.port)
        self.ftp.login(self.username, self.password)
        return self.ftp

    def disconnect(self):
        if self.ftp is not None:
            self.ftp.close()

    def get_instance(self):
        return self.ftp

    def process_exception(self, err):
        error_info = str(err).split(None, 1)
        print(error_info)

    def is_connected(self):
        connect_status = False
        if self.ftp is not None:
            try:
                self.ftp.voidcmd("NOOP")
                connect_status = True
            except ftplib.all_errors as e:
                self.process_exception(e)
                connect_status = False
        return connect_status

    def delete_file(self, remote_file_path, show_log=True):
        del_success = True
        try:
            self.connect()
            self.ftp.delete(remote_file_path)
            if show_log:
                print(f"Success to delete remote file[{remote_file_path}]")
        except ftplib.all_errors as e:
            self.process_exception(e)
            del_success = False
            if show_log:
                print(f"Fail to delete remote file[{remote_file_path}]")
        finally:
            self.disconnect()
        return del_success

    def upload_file(self, remote_file_path, local_file_path, del_exists=True):
        """
        从本地上传文件到ftp
        :param remote_file_path: 远程文件完整路径名
        :param local_file_path: 本地文件完整路径名
        :param del_exists: 为True时，若远程文件已存在，则删除远程文件
        :return: 上传成功则返回True，上传失败则返回False
        """
        upload_success = True
        try:
            if del_exists:
                self.delete_file(remote_file_path, show_log=False)

            self.connect()
            tmp_remote_path = f"{remote_file_path}.TMP"
            with open(local_file_path, 'rb') as fp:
                self.ftp.storlines(f'STOR {tmp_remote_path}', fp)
            self.ftp.rename(tmp_remote_path, remote_file_path)
            print(f"Success to upload file from [{local_file_path}] to [{remote_file_path}]!")
        except ftplib.all_errors as e:
            self.process_exception(e)
            upload_success = False
            print(f"Fail to upload file from [{local_file_path}] to [{remote_file_path}]!")
        finally:
            self.disconnect()
        return upload_success

    def rename(self, from_file_name, to_file_name):
        rename_success = True
        try:
            self.connect()
            self.ftp.rename(from_file_name, to_file_name)
            print(f"Success to rename from [{from_file_name}] to [{to_file_name}] on FTP Server!")
        except ftplib.all_errors as e:
            self.process_exception(e)
            rename_success = False
            print(f"Fail to rename from [{from_file_name}] to [{to_file_name}] on FTP Server!")
        finally:
            self.disconnect()
        return rename_success

    def download_single_file(self, remote_file_path, local_file_path, need_delete=False):
        """
        从远程下载文件到本地
        :param remote_file_path: 远程文件完整路径名
        :param local_file_path: 本地文件完整路径名
        :param need_delete: 下载完成后是否删除远程文件
        :return:
        """
        dl_success = True
        try:
            self.connect()
            with open(local_file_path, 'wb') as f:
                filename = 'RETR ' + remote_file_path
                self.ftp.retrbinary(filename, f.write)
            print(f"Success to download file from {remote_file_path} to {local_file_path}")
            if need_delete:
                self.delete_file(remote_file_path)
        except ftplib.all_errors as e:
            self.process_exception(e)
            dl_success = False
            print(f"Fail to download file from {remote_file_path} to {local_file_path}")
        finally:
            self.disconnect()
        return dl_success

    def download_multi_file(self, remote_dir_path, local_dir_path, need_delete=False):
        """
        批量下载远程目录下所有文件至本地目录
        :param remote_dir_path: 远程目录完整路径名
        :param local_dir_path: 本地目录完整路径名
        :param need_delete: 下载完成后是否删除远程文件
        :return: 返回下载后的文件名列表
        """
        file_path_list = []
        try:
            self.connect()
            self.ftp.cwd(remote_dir_path)
            file_list = self.ftp.nlst()
            for name in file_list:
                file_path = local_dir_path + "/" + name
                f = open(file_path, 'wb')
                filename = 'RETR ' + name
                self.ftp.retrbinary(filename, f.write)
                print(f"Success to download remote file: {name}")
                f.close()
                if need_delete:
                    self.ftp.delete(name)
                file_path_list.append(file_path)
        except ftplib.all_errors as e:
            self.process_exception(e)
            print(f"Fail to download from remote dir: {remote_dir_path}")
        finally:
            self.disconnect()

        return file_path_list

    def remove_dir(self, dir_path):
        try:
            self.connect()
            self.ftp.rmd(dir_path)
        except ftplib.all_errors as e:
            self.process_exception(e)
        finally:
            self.disconnect()

    def __del__(self):
        self.ftp.close()


