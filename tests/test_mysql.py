import os
from pathlib import Path
import pymysql
import pymysql.cursors
import time

work_dir = "/ndyd/apps/athena/etl/export"
file_name_list = os.listdir(work_dir)

session: pymysql.Connection = pymysql.connect(host="localhost", port=3306, user="root", password="Ndyd@2024",
                                              database="athena", charset="UTF8MB4")
session.autocommit(True)
# load
with session.cursor() as cursor:
    for file_name in file_name_list:
        tb_name = Path(file_name).stem
        sql = f"truncate table {tb_name}"
        resp = cursor.execute(sql)
        print(f"{sql}: {resp}")
        file_path = f"{work_dir}/{file_name}"
        ld_sql = f"load data infile '{file_path}' replace into table athena.{tb_name} " \
                 f"character set UTF8MB4 fields terminated by '|' lines terminated by '\n'"
        b_t = time.time()
        resp = cursor.execute(ld_sql)
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to execute SQL:[{ld_sql}], the affected rows: {resp}")

# check
with session.cursor() as cursor:
    for file_name in file_name_list:
        tb_name = Path(file_name).stem
        sql = f"select count(1) as cnt from {tb_name}"
        b_t = time.time()
        row_cnt = cursor.execute(sql)
        rows = cursor.fetchall()
        if rows is not None and len(rows) > 0:
            row_cnt = rows[0][0]
        e_t = time.time()
        print(f"It has took {round(e_t - b_t, 3)}s to execute SQL:[{sql}], the affected rows: {row_cnt}")

session.close()
