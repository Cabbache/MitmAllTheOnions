#!/bin/sh

set -e
export REDIS=$(getent hosts redis | awk '{print $1}')
python -u /handler.py
