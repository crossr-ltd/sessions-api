import json
from decimal import Decimal
from typing import List

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from app.api.models.domains import Session
from app.api.utils.db import get_db

db: ServiceResource = get_db()


def get_all_sessions():
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.scan()  # scan all data
    return response.get('Items', [])  # return data


def get_all_sessions_metadata(user_id):
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.scan()  # scan all data
    sessions = response.get('Items', [])
    return [session.get('metadata', {}) for session in sessions if session.get('metadata', {}).get('user_id', '') == str(user_id)]


def get_session(id: str):
    try:
        table = db.Table('Sessions')  # referencing to table Sessions
        response = table.get_item(Key={'id': id})  # get session using id (partition key)
        return response['Item']  # return single data
    except ClientError as e:
        raise ValueError(e.response['Error']['Message'])


def update_session(session: Session):
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.update_item(  # update single item
        Key={'id': session.id},  # using partition key specifying which attributes will get updated
        UpdateExpression="""                
            set
                positions=:positions,
                data_imports=:data_imports
        """,
        ExpressionAttributeValues={  # values defined in here will get injected to update expression
            ':positions': [dict(position) for position in session.positions],
            ':data_imports': [dict(data_import) for data_import in session.data_imports]
        },
        ReturnValues="UPDATED_NEW"  # return the newly updated data point
    )
    return response


def create_session(session: Session):
    session_dict = session.dict()
    session = json.loads(json.dumps(session_dict), parse_float=Decimal)
    table = db.Table('Sessions')
    response = table.put_item(Item=session)
    return response

def delete_session(id: str):
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.delete_item(  # delete session using id
        Key={'id': id}
    )
    return response
