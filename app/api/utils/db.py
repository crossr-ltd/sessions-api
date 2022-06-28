import os

import boto3
from boto3.resources.base import ServiceResource
from dotenv import load_dotenv

load_dotenv()


def initialize_db() -> ServiceResource:
    ddb = boto3.resource('dynamodb',
                         endpoint_url='http://localhost:8000',
                         region_name='us-east-1',
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         aws_secret_access_key='example')
    return ddb


db = initialize_db()


def get_db() -> ServiceResource:
    return db
