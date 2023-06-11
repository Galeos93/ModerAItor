from abc import ABC, abstractmethod
import json

import boto3
from botocore.errorfactory import ClientError

from moderaitor.models import base_model_to_dynamo_item

class DatabaseProvider(ABC):
    @abstractmethod
    def save_object(self, object_data: dict):
        pass

class DynamoDBProvider(DatabaseProvider):
    def __init__(self, table_name: str):
        # Initialize the DynamoDB client
        self.dynamodb_client = boto3.client("dynamodb")
        self.table_name = table_name

    def create_table(self):
        try:
            self.dynamodb_client.create_table(
                TableName=self.table_name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S',
                    }
                ],
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH',
                    }
                ],
                BillingMode='PAY_PER_REQUEST',
            )
        except ClientError as exc:
            if exc.response["Error"]["Code"] != "ResourceInUseException":
                raise

    def save_object(self, object_data: dict) -> bool:
        # Save the object to DynamoDB table
        item = base_model_to_dynamo_item(object_data)

        _ = self.dynamodb_client.put_item(
            TableName=self.table_name,
            ReturnConsumedCapacity='TOTAL',
            ReturnValues='ALL_OLD',
            Item=item
        )

        print(f"Object saved to DynamoDB table: {self.table_name}")


class AWSS3Provider(DatabaseProvider):
    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client('s3')
        self.bucket_name = bucket_name

    def create_bucket(self):
        try:
            self.s3_client.create_bucket(
                ACL="private",
                Bucket=self.bucket_name
            )
        except ClientError as exc:
            print(exc)
            if exc.response["Error"]["Code"] != "BucketAlreadyExists":
                raise

    def save_object(self, object_data: dict) -> bool:
        # Save the object to DynamoDB table
        json_data = json.dumps(object_data).encode('utf-8')
        self.s3_client.put_object(
            Body=json_data,
            Bucket=self.bucket_name,
            Key=object_data['id']
        )

        print(f"Object saved to S3 bucket: {self.bucket_name}")
