import boto3
import os
from dotenv import load_dotenv

load_dotenv()

region_name = os.getenv("region_name")
aws_access_key_id = os.environ.get("aws_access_key")
aws_secret_access_key = os.environ.get("aws_secret_access_key")


def create_table(
    table_name: str, key_schema: list[dict], **columns: dict[dict]
) -> None:

    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name,
    )

    # Create the table with initial provisioned capacity units (optional, adjust as needed)
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=list(columns.items()),
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    print(f"Table '{table_name}' created successfully!")


table_key_schema = [{"AttributeName": "Email", "KeyType": "HASH"}]

columns = {"Email": {"AttributeType": "S"}}

create_table("subscribers", table_key_schema, **columns)
