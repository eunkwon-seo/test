require('dotenv').config(); // 환경 변수 로드
const express = require('express');
const cors = require('cors');

const Database = require('./utils/database'); // DB 로직
const authRoutes = require('./routes/auth'); // 인증 라우트

const app = express();

app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());



app.get('/health', async (req, res) => {
  try {
      const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
      const client = new DynamoDBClient({
          region: process.env.AWS_REGION,
          credentials: {
              accessKeyId: process.env.AWS_ACCESS_KEY_ID,
              secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY
          }
      });
      
      await client.config.credentials();
      res.status(200).json({
          status: 'healthy',
          message: 'DynamoDB connection successful',
          // table: process.env.PERFORMANCE_TABLE
      });
  } catch (error) {
      res.status(500).json({
          status: 'unhealthy',
          message: 'DynamoDB connection failed',
          error: error.message
      });
  }
});


const db = new Database();

// 라우트 설정
app.use('/api/auth', authRoutes(db));


// 에러 핸들링
app.use((err, req, res, next) => {
    console.error('Server Error:', err);
    res.status(500).json({ error: 'Internal Server Error', details: err.message });
  });

  
// 공통 환경변수에서 PORT 가져오기
const PORT = process.env.AUTH_PORT || 5002;
app.listen(PORT, () => {
  console.log(`Auth 서비스가 ${PORT} 포트에서 실행 중입니다.`);
});


module.exports = app;
