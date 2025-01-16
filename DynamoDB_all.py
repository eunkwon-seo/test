import boto3
import csv
from botocore.exceptions import ClientError

def create_dynamodb_table():
    """DynamoDB 테이블 생성 (On-Demand 모드)"""
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id='AKIAS74TMBNFXNNU7UWU',
        aws_secret_access_key='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',
        region_name='ap-northeast-2'
    )

    table_name = "Performances_info"

    try:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {'AttributeName': 'performance_id', 'KeyType': 'HASH'},  # 파티션 키
            ],
            AttributeDefinitions=[
                {'AttributeName': 'performance_id', 'AttributeType': 'S'},  # String 타입
            ],
            BillingMode='PAY_PER_REQUEST'  # On-Demand 모드
        )

        print(f"Table {table_name} is being created. Please wait...")
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"Table {table_name} has been created successfully in On-Demand mode!")

    except ClientError as e:
        # 테이블이 이미 존재하는 경우 처리
        if e.response['Error']['Code'] == 'ResourceInUseException':
            print(f"Table '{table_name}' already exists. Proceeding without creating a new one.")
        else:
            print(f"Failed to create table '{table_name}': {e.response['Error']['Message']}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def upload_to_dynamodb(file_name, table_name):
    """DynamoDB에 CSV 데이터를 업로드"""
    # DynamoDB 리소스 생성
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id='AKIAS74TMBNFXNNU7UWU',
        aws_secret_access_key='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',
        region_name='ap-northeast-2'
    )
    # DynamoDB 테이블 참조
    table = dynamodb.Table(table_name)

    try:
        # CSV 파일 읽기
        with open(file_name, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # 각 행을 DynamoDB에 삽입
                item = {
                    "performance_id": row["performance_id"],
                    "image": row["image"],
                    "title": row["title"],
                    "genre": row["genre"],
                    "city": row["city"],
                    "start_date": row["start_date"],
                    "end_date" : row["end_date"],
                    "location" : row["location"],
                    "age": row["age"],
                    "price": row["price"],
                    "site": row["site"],
                    "link": row["link"],

                }
                # DynamoDB에 삽입
                table.put_item(Item=item)
                print(f"Inserted row: {item}")

        print(f"All data from {file_name} has been uploaded to DynamoDB table {table_name}.")

    except Exception as e:
        print(f"Failed to upload data to DynamoDB: {e}")


if __name__ == "__main__":
    # DynamoDB 테이블 생성
    create_dynamodb_table()

    # CSV 데이터를 업로드
    csv_file_path = "/app/Performances.csv"  # CSV 파일 경로
    table_name = "Performances_info"
    upload_to_dynamodb(csv_file_path, table_name)
