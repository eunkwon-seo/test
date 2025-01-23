const AWS = require('aws-sdk');

// AWS DynamoDB 설정
AWS.config.update({
    region: process.env.AWS_REGION,
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    // endpoint: process.env.DYNAMODB_ENDPOINT, // 로컬 테스트용
});

const dynamoClient = new AWS.DynamoDB.DocumentClient();

module.exports = dynamoClient;