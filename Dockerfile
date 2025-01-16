# Python 3.10 slim 이미지를 기반으로 사용
FROM python:3.10-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libexpat1 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxrandr2 \
    libgbm1 libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0 \
    libgtk-3-0 wget curl fonts-ipafont fonts-ipaexfont tzdata


# 로케일 및 시간대 설정
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Asia/Seoul

# 작업 디렉토리 설정
WORKDIR /app

# Python 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir playwright && \
    playwright install --with-deps

# 프로젝트 복사
COPY . .

# 실행 스크립트 권한 부여
RUN chmod +x run_all.sh

# 기본 실행 명령어 설정
CMD ["bash", "run_all.sh"]
