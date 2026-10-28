#!/bin/bash
# 5분마다 collect.py 실행, 23:55 KST까지
cd "$(dirname "$0")"
export SEOUL_API_KEY=$(cat .key)
while [ "$(date +%H%M)" -lt 2355 ]; do
  /opt/homebrew/bin/python3 collect.py >> collect.log 2>&1
  sleep $(( 300 - $(date +%s) % 300 ))
done
