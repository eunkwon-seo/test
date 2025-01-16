#!/bin/bash

# Bash 스크립트 시작
echo "Starting Python scripts execution..."

# Python 파일을 백그라운드에서 실행
python Musical.py &
python Korea_Music.py &
python Popular_Music.py &
python Classical.py &

# 모든 백그라운드 프로세스가 종료될 때까지 대기
wait

echo "Background Python scripts completed."

# DynamoDB.py 실행
python DynamoDB_all.py

echo "All scripts have been executed successfully!"