import boto3
import os
from validate_email import validate_email
import sys
from dotenv import load_dotenv

load_dotenv()

class Subscriber:

    aws_access_key_id = os.environ.get("aws_access_key")
    aws_secret_access_key = os.environ.get("aws_secret_access_key")
    region_name = os.getenv("region_name")

    def __init__(self, email: str) -> None:
        self.email = email
        self._ddb_data = self.get_ddb_data()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        while True:
            is_valid = validate_email(email)
            if is_valid:
                self._email = email
                break
            print("Invalid email address")
            email = input("Enter your email address: ")

    @classmethod
    def get(cls) -> str:
        email = input("Enter your email address: ")
        return cls(email)

    def get_ddb_data(self) -> list[str]:
        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=Subscriber.aws_access_key_id,
            aws_secret_access_key=Subscriber.aws_secret_access_key,
            region_name=Subscriber.region_name
        )

        table = dynamodb.Table("subscribers")
        response = table.scan()
        items = response["Items"]
        data = [d["Email"] for d in items]
        return data

    def add_subscriber(self) -> None:
        """
        Adds a new subscriber to DynamoDB
        :param email: email address of the new subscriber
        """
        subs = []
        while True:
            try:
                if (self.email in self._ddb_data) or (self.email in subs):
                    print("You are a subscriber already!")
                else:
                    dynamodb = boto3.resource(
                        "dynamodb",
                        aws_access_key_id=Subscriber.aws_access_key_id,
                        aws_secret_access_key=Subscriber.aws_secret_access_key,
                        region_name=Subscriber.region_name,
                    )

                    item = {"Email": self.email}
                    table = dynamodb.Table("subscribers")
                    table.put_item(Item=item)
                    print(f"Email '{self.email}' was added successfully to the subscribers list!")
                    subs.append(self.email)
                self.email = input("Enter your email address: ")
            except KeyboardInterrupt:
                sys.exit()

    def remove_subscriber(self) -> None:
        """Removes a subscriber from DynamoDB"""
        removed_subs = []
        while True:
            if (self.email not in self._ddb_data) or (self.email in removed_subs):
                print("You are not a subscriber")
                self.email = input("Enter email address to delete: ")
            else:
                dynamodb = boto3.resource(
                    "dynamodb",
                    aws_access_key_id=Subscriber.aws_access_key_id,
                    aws_secret_access_key=Subscriber.aws_secret_access_key,
                    region_name=Subscriber.region_name,
                )

                delete_key = {"Email": self.email}
                table = dynamodb.Table("subscribers")
                table.delete_item(Key=delete_key)
                print(f"Email '{self.email}' was deleted successfully")
                removed_subs.append(self.email)
                break
