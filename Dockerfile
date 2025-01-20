# 1단계: Node.js를 사용해 React 앱을 빌드
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./

# Sass와 Babel 문제를 해결하기 위해 의존성 설치
RUN npm install --legacy-peer-deps
RUN npm install -g @aws-amplify/cli
RUN npm install ajv ajv-keywords
RUN npm install amazon-cognito-identity-js
RUN npm install jwt-decode
RUN yum update -y && \
    yum install -y \
    aws-cli \
    unzip && \
    yum clean all

COPY . .

RUN npm run build

# 2단계: Nginx를 사용해 정적 파일 제공
FROM nginx:alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf


COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
