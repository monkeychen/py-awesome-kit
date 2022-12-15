import time
import paramiko
from awekit import base


class SshClient(object):
    # 创建一个ssh的白名单
    know_host = paramiko.AutoAddPolicy()

    def __init__(self, host, port=22, user=None, password=None, auto_connect=True):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auto_connect = auto_connect
        self.ssh_client = None
        self.sftp_client = None
        if auto_connect:
            self.ssh_client = self.connect()

    def connect(self):
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(self.know_host)
        self.ssh_client.connect(hostname=self.host, port=self.port, username=self.user, password=self.password)
        return self.ssh_client

    def get_internal_ssh_client(self):
        return self.ssh_client

    def disconnect(self):
        if self.ssh_client is not None:
            self.ssh_client.close()

    def open_sftp_client(self):
        self.sftp_client = self.ssh_client.open_sftp()
        return self.sftp_client

    def close_sftp_client(self):
        if self.sftp_client is not None:
            self.sftp_client.close()

    def exec_command(self, cmd: str, timeout=None, encoding=base.UTF_8, use_sudo=False):
        stdin, stdout, stderr = self.ssh_client.exec_command(cmd, timeout=timeout, get_pty=use_sudo)
        if use_sudo:
            stdin.write(self.password + '\n')
            stdin.flush()
        if stdout is not None:
            print(stdout.read().decode(encoding=encoding))
        elif stderr is not None:
            print(stderr.read().decode(encoding=encoding))

    def upload(self, local_file_path: str, remote_file_path: str):
        b_t = time.time()
        sftp = self.ssh_client.open_sftp()
        file_attrs = sftp.put(local_file_path, remote_file_path)
        e_t = time.time()
        print(f"It took {round(e_t - b_t, 2)}s to upload from local[{local_file_path}] to remote[{remote_file_path}], file attrs:{file_attrs}")
        sftp.close()

    def download(self, local_file_path: str, remote_file_path: str):
        b_t = time.time()
        sftp = self.ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        e_t = time.time()
        print(f"It took {round(e_t - b_t, 2)}s to download from remote[{remote_file_path}] to local[{local_file_path}]!")
        sftp.close()

    def transport_upload(self, local_file_path: str, remote_file_path: str):
        b_t = time.time()
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.user, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        file_attrs = sftp.put(local_file_path, remote_file_path)
        e_t = time.time()
        print(f"[transport_upload] ==> It took {round(e_t - b_t, 2)}s to upload from local[{local_file_path}] to remote[{remote_file_path}], "
              f"file attrs:{file_attrs}")
        transport.close()
        sftp.close()

    def transport_download(self, local_file_path: str, remote_file_path: str):
        b_t = time.time()
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.user, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.get(remote_file_path, local_file_path)
        e_t = time.time()
        print(f"[transport_download] ==> It took {round(e_t - b_t, 2)}s to download from remote[{remote_file_path}] to local[{local_file_path}]!")
        transport.close()
        sftp.close()
