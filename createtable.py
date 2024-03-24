import boto3
import os


def create_table(
    table_name: str, key_schema: list[dict], **columns: dict[dict]
) -> None:

    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ.get("aws_access_key"),
        aws_secret_access_key=os.environ.get("aws_secret_access_key"),
        region_name="us-east-1",
    )

    # Create the table with initial provisioned capacity units (optional, adjust as needed)
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=key_schema,
        AttributeDefinitions=list(columns.items()),
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )

    # Print a confirmation message
    print(f"Table '{table_name}' created successfully!")


table_key_schema = [{"AttributeName": "Email", "KeyType": "HASH"}]

columns = {"Email": {"AttributeType": "S"}}

create_table("subscribers", table_key_schema, **columns)