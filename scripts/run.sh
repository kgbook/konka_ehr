#!/usr/bin/env bash

workdir=$(cd $(dirname $0); pwd)
topdir=$workdir/..

python3_path=$(which python3)
if [ -z "$python3_path" ]; then
  echo "python3 not found"
  exit 1
fi

pip3_path=$(which pip3)
if [ -z "$pip3_path" ]; then
  echo "pip3 not found"
  exit 1
fi

pushd $topdir
$pip3_path install -r requirements.txt
$python3_path konka_qianka.py
popd