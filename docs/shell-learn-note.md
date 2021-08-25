# Shell学习笔记

## 1. 进入脚本所在目录
```shell
# work_dir="/home/chenzhian/workspace/account-encoder/mobile"
# cd $(echo work_dir)
work_dir=$(cd $(dirname $0); pwd)

if [ "$#" -ne "1" ]; then
    echo "Usage $0 <yyyyMM>"
    exit 1
fi
month_id=$1
# month_id=${month_id:=$(date +%Y%m -d "-1 months")}

echo "The target month_id=${month_id}"
```