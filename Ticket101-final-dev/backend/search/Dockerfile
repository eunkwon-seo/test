FROM node:18-alpine

WORKDIR /usr/src/app

# 패키지 파일 복사 및 의존성 설치
COPY package.json ./
RUN npm install --only=production
RUN npm install -g @aws-amplify/cli
RUN npm install -g @aws-sdk/lib-dynamodb

# AWS SDK 설치
RUN npm install aws-sdk

# 소스 코드 복사
COPY . .

# 환경 변수 설정
EXPOSE ${SEARCH_PORT}
CMD ["node", "app.js"]