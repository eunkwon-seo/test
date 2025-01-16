require('dotenv').config(); // 환경 변수 로드
const express = require('express');
const cors = require('cors');

const Database = require('./utils/database'); // DB 로직
const surveyRoutes = require('./routes/surveyRoutes'); // 인증 라우트

const app = express();

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));

app.use(express.json());

// const db = new Database();

// 라우트 설정

const db = new Database();

app.use('/api/survey', surveyRoutes(db));

// 에러 핸들링
app.use((err, req, res, next) => {
  console.error('Server Error:', err);
  res.status(500).json({ error: 'Internal Server Error', details: err.message });
});


// 공통 환경변수에서 PORT 가져오기
const PORT = process.env.SURVEY_PORT || 5003;
app.listen(PORT, () => {
  console.log(`Survey 서비스가 ${PORT} 포트에서 실행 중입니다.`);
});

module.exports = app;
