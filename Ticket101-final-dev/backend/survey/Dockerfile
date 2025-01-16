# Node.js 18 기반 경량 Alpine 이미지 사용
FROM node:18-alpine

# 작업 디렉토리 설정
WORKDIR /usr/src/app

# 패키지 파일 복사 및 의존성 설치
COPY package.json ./
RUN npm install --production

# 소스 코드 복사
COPY . .

# 컨테이너 포트 노출
EXPOSE ${APP_PORT}

# 애플리케이션 실행
CMD ["node", "app.js"]