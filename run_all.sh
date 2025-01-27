#!/bin/bash

# Bash 스크립트 시작
echo "Starting Python scripts execution..."

# Python 파일을 백그라운드에서 실행
python Musical.py &
p1=$!
python Korea_Music.py &
p2=$!
python Popular_Music.py &
p3=$!
python Classical.py &
p4=$!

# 모든 백그라운드 프로세스가 종료될 때까지 대기
wait $p1 $p2 $p3 $p4 || { echo "Error occurred in one of the scripts"; exit 1; }

echo "Background Python scripts completed."

# DynamoDB.py 실행
python DynamoDB_all.py || { echo "Error occurred in DynamoDB_all.py"; exit 1; }

echo "All scripts have been executed successfully!"