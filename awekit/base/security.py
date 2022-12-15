from cryptography.fernet import Fernet
import joblib
import os


class Cryptography(object):

    def __init__(self):
        pk_dir_path = f"{os.getcwd()}/temp"
        if not os.path.exists(pk_dir_path):
            os.mkdir(pk_dir_path)
        self.pk_path = f"{pk_dir_path}/pkey.bin"
        if not os.path.exists(self.pk_path):
            self.generate_pk()
        cipher_key = joblib.load(self.pk_path)
        self.cipher = Fernet(cipher_key)

    def generate_pk(self):
        cipher_key = Fernet.generate_key()
        print(f"The generated private-key is: {cipher_key}")
        joblib.dump(cipher_key, self.pk_path)

    def encrypt(self, pure_content: str):
        return self.cipher.encrypt(pure_content.encode()).decode()

    def decrypt(self, encrypted_content: str):
        return self.cipher.decrypt(encrypted_content.encode()).decode()
