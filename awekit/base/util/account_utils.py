import re
import pandas as pd


class AccountUtils(object):

    def encode_single(self, account):
        encode_account = ''
        for c in list(account):
            encode_account = encode_account + str(ord(c))
        return encode_account

    def decode_single(self, encode_account):
        account = ''
        for c in re.findall('.{2}', encode_account):
            account = account + chr(int(c))
        return account

    def encode_multi(self, account_list):
        result = []
        for account in account_list:
            result.append(self.encode_single(account))
        return result

    def decode_multi(self, encode_account_list):
        result = []
        for encode_account in encode_account_list:
            result.append(self.decode_single(encode_account))
        return result

    def decode_from_file(self, in_csv_file_path, out_csv_file_path):
        df = pd.read_csv(in_csv_file_path)
        df = df.drop(columns=['地市'])
        res = self.decode_multi(df['ID'].values)
        df['ORI_ID'] = pd.DataFrame(res)
        df.to_csv(out_csv_file_path, index=False)


if __name__ == '__main__':
    account_utils = AccountUtils()
    ori_account_list = account_utils.decode_multi(['49515653485148544852544849', '49515653485154495554484849'])
    print(ori_account_list)
    account_utils.decode_from_file('E:/tmp/user_id.csv', 'E:/tmp/out_user_id.csv')
