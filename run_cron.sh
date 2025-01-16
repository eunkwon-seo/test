#!/bin/bash

# 로그 파일 경로
LOG_FILE="/home/test/my_crawler_project/ecr_cron.log"

# AWS ECR 정보
AWS_REGION="ap-northeast-2"
ECR_URI="205930629963.dkr.ecr.ap-northeast-2.amazonaws.com/test2:latest"

# 로그 시작
echo "[$(date)] Starting ECR Cron Job..." | tee -a $LOG_FILE

# 1. ECR 로그인
echo "[$(date)] Logging into ECR..." | tee -a $LOG_FILE
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Failed to log in to ECR. Exiting." | tee -a $LOG_FILE
    exit 1
fi
echo "[$(date)] Successfully logged into ECR." | tee -a $LOG_FILE

# 2. 최신 Docker 이미지 가져오기
echo "[$(date)] Pulling the latest Docker image from ECR..." | tee -a $LOG_FILE
docker pull $ECR_URI >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Failed to pull Docker image. Exiting." | tee -a $LOG_FILE
    exit 1
fi
echo "[$(date)] Successfully pulled the Docker image." | tee -a $LOG_FILE

# 3. 기존 컨테이너 중지 및 삭제 (있다면)
echo "[$(date)] Cleaning up old containers..." | tee -a $LOG_FILE
docker stop crawler_container >> $LOG_FILE 2>&1 || true
docker rm crawler_container >> $LOG_FILE 2>&1 || true
echo "[$(date)] Old containers cleaned up." | tee -a $LOG_FILE

# 4. 컨테이너 실행
echo "[$(date)] Starting new Docker container..." | tee -a $LOG_FILE
container_id=$(docker run -d --name crawler_container $ECR_URI 2>> $LOG_FILE)
if [ $? -ne 0 ]; then
    echo "[$(date)] Failed to start Docker container. Exiting." | tee -a $LOG_FILE
    exit 1
fi
echo "[$(date)] Docker container started: $container_id" | tee -a $LOG_FILE

# 5. 1시간 동안 실행
echo "[$(date)] Waiting for 1 hour..." | tee -a $LOG_FILE
sleep 3600

# 6. 컨테이너 중지 및 삭제
echo "[$(date)] Stopping and removing Docker container..." | tee -a $LOG_FILE
docker stop $container_id >> $LOG_FILE 2>&1
docker rm $container_id >> $LOG_FILE 2>&1
if [ $? -ne 0 ]; then
    echo "[$(date)] Failed to stop or remove Docker container. Check logs for details." | tee -a $LOG_FILE
else
    echo "[$(date)] Docker container stopped and removed successfully." | tee -a $LOG_FILE
fi

# 로그 종료
echo "[$(date)] ECR Cron Job Completed." | tee -a $LOG_FILE