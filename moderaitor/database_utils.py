from abc import ABC, abstractmethod

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
                    # {
                    #     'AttributeName': 'username',
                    #     'AttributeType': 'S',
                    # },
                    # {
                    #     'AttributeName': 'body',
                    #     'AttributeType': 'S',
                    # },
                    # {
                    #     'AttributeName': 'flag',
                    #     'AttributeType': 'S',
                    # },
                    # {
                    #     'AttributeName': 'context',
                    #     'AttributeType': 'S',
                    # },
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
