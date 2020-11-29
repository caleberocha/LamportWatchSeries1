#!/bin/bash
LOG_DIR=logs

cd $(dirname $0)/..

python3 log_api.py download $LOG_DIR 1 2 3 4 5
python3 utils/log_joiner.py $LOG_DIR