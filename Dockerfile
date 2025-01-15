# 베이스 이미지 설정 (Python, Node.js 등 필요에 맞게 변경 가능)
FROM nginx:latest

# Nginx에 HTML 파일 복사
COPY index.html /usr/share/nginx/html

# 컨테이너가 실행될 때 기본으로 사용할 명령어
CMD ["nginx", "-g", "daemon off;"]
