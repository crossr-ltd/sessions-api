import os

import boto3
from dotenv import load_dotenv

from app.constants import AWS_REGION_NAME

load_dotenv()


def generate_table(ddb, table_name: str):
    ddb = boto3.resource('dynamodb',
                         endpoint_url=os.getenv('ENDPOINT_URL'),
                         region_name=AWS_REGION_NAME,
                         # note that if you create a table using different region name and aws key
                         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                         # you won't see this table on the admin app
                         aws_secret_access_key=('AWS_SECRET_ACCESS_KEY', 'example'))

    ddb.create_table(
        TableName=table_name,  # create table
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',  # In this case, I only specified uid as partition key (there is no sort key)
                'AttributeType': 'S'  # with type string
            }
        ],
        KeySchema=[
            {
                'AttributeName': 'uid',  # attribute uid serves as partition key
                'KeyType': 'HASH'
            }
        ],
        ProvisionedThroughput={  # specying read and write capacity units
            'ReadCapacityUnits': 10,  # these two values really depend on the app's traffic
            'WriteCapacityUnits': 10
        }
    )
    print(f'Successfully created table {table_name}')
