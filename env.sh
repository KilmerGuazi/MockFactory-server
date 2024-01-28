#!/usr/bin/env bash

ENV=$1
if [ ! ${ENV} ]
then
    ENV=local
fi
echo ${ENV}
export FLASK_CONFIG=${ENV}  # 当前环境 可选 local product dev test
