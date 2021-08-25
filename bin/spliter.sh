#!/bin/bash

# usage: ./spliter.sh tmp_data_1615986750790.csv 泉州 quanzhou
mkdir $3
target_csv=$3".csv"
prefix=$3"_"
cat $1 | grep $2 > $target_csv
split -l 50000 $target_csv -d -a 3 $3/$prefix
cd $3
ls|grep $prefix|xargs -n1 -i{} mv {} {}.csv
for f in `ls .`
do
  iconv -f UTF-8 -t GBK $f > "gbk_"$f
  rm -f $f
done
#mv $3"_*" ./$3
cd ..
zip -r $3".zip" ./$3
rm -rf ./$3
rm -f $target_csv
