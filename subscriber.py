import boto3
import os
from validate_email import validate_email


class Subscriber:

    def __init__(self, email: str) -> None:
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        while True:
            is_valid = validate_email(email)  # , verify=True)
            if is_valid:
                self._email = email
                break
            else:
                print("Invalid email address")
                email = input("Enter your email address: ")

    @classmethod
    def get(cls) -> str:
        email = input("Enter your email address: ")
        return cls(email)

    def add_subscriber(self) -> None:
        """
        Adds a new subscriber to DynamoDB
        :param email: email address of the new subscriber
        """
        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=os.environ.get("aws_access_key"),
            aws_secret_access_key=os.environ.get("aws_secret_access_key"),
            region_name="us-east-1",
        )

        item = {"Email": self.email}
        table = dynamodb.Table("subscribers")
        table.put_item(Item=item)
        print(f"Email '{self.email}' added successfully")

    def remove_subscriber(self, email_address) -> None:
        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=os.environ.get("aws_access_key"),
            aws_secret_access_key=os.environ.get("aws_secret_access_key"),
            region_name="us-east-1",
        )

        while True:
            delete_key = {"Email": email_address}
            table = dynamodb.Table("subscribers")
            response = table.delete_item(Key=delete_key)

            if "DeletedItems" in response:
                print(f"Email '{email_address}' deleted successfully")
            else:
                print(f"Email '{email_address}' not found in the table")
                email_address = input("Enter email address to delete: ")