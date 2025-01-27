FROM node:18-alpine

WORKDIR /usr/src/app

# 패키지 파일 복사 및 의존성 설치
COPY package.json ./
RUN npm install --only=production
RUN npm install -g @aws-amplify/cli @aws-sdk/lib-dynamodb aws-sdk

# 빌드 환경 변수 선언 및 확인

ARG ACCESS_KEY_ID
ENV ACCESS_KEY_ID=$ACCESS_KEY_ID

ARG SECRET_ACCESS_KEY
ENV SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY

RUN echo "ACCESS_KEY_ID=$ACCESS_KEY_ID" && echo "SECRET_ACCESS_KEY=$SECRET_ACCESS_KEY"

# 소스 코드 복사
COPY . .

# 포트 노출 및 실행
EXPOSE 5007
CMD ["node", "app.js"]
