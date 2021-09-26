import os
import sys
import zipfile


class Compression(object):

    def __init__(self):
        pass

    @classmethod
    def zip_dir(cls, src_dir_path, dest_file_path, include_dir=True, compression=zipfile.ZIP_STORED):
        zip_file = zipfile.ZipFile(dest_file_path, mode='w', compression=compression)
        for dir_path, dirname_list, filename_list in os.walk(src_dir_path):
            if include_dir:
                f_path = dir_path.replace(os.path.dirname(src_dir_path), "")
            else:
                f_path = dir_path.replace(src_dir_path, "")
            f_path = f_path and f_path + os.sep or ''
            for filename in filename_list:
                zip_file.write(os.path.join(dir_path, filename), f_path + filename)
        zip_file.close()
        return dest_file_path


if __name__ == '__main__':
    Compression().zip_dir(sys.argv[1], sys.argv[2])

