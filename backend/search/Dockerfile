FROM node:18-alpine

WORKDIR /app

# 패키지 파일 복사 및 의존성 설치
COPY package.json ./
RUN npm install --only=production
RUN npm install -g @aws-amplify/cli
RUN npm install -g @aws-sdk/lib-dynamodb
ARG FRONTEND_URL
ENV FRONTEND_URL=$FRONTEND_URL
# AWS SDK 설치
RUN npm install aws-sdk

# 소스 코드 복사
COPY . .

# 환경 변수 설정
EXPOSE 5006
CMD ["node", "app.js"]