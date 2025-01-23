const AWS = require('aws-sdk');
require('dotenv').config();

// AWS DynamoDB 설정
AWS.config.update({
  region: process.env.AWS_REGION, // AWS 리전 설정
  accessKeyId: process.env.AWS_ACCESS_KEY_ID,   // 환경 변수에서 가져오기
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY, // 환경 변수에서 가져오기
});

const dynamoClient = new AWS.DynamoDB.DocumentClient();

module.exports = dynamoClient;
