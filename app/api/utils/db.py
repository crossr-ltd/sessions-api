import os

import boto3
from boto3.resources.base import ServiceResource
from dotenv import load_dotenv

load_dotenv()


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
                         endpoint_url=os.getenv('ENDPOINT_URL'),
                         region_name=os.getenv('AWS_REGION_NAME'),
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    return ddb


db = initialize_db()


def get_db() -> ServiceResource:
    return db
