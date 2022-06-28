from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from app.api.model.model import Session
from app.api.utils.db import get_db

db: ServiceResource = get_db()


def get_all_sessions():
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.scan()  # scan all data
    return response.get('Items', [])  # return data


def get_session(session_id: str):
    try:
        table = db.Table('Sessions')  # referencing to table Sessions
        response = table.get_item(Key={'session_id': session_id})  # get session using id (partition key)
        return response['Item']  # return single data
    except ClientError as e:
        raise ValueError(e.response['Error']['Message'])


def update_session(session: Session):
    table = db.Table('Session')  # referencing to table Sessions
    response = table.update_item(  # update single item
        Key={'uid': session.session_id},  # using partition key specifying which attributes will get updated
        UpdateExpression="""                
            set
                positions=:positions,
                data_imports=:data_imports
        """,
        ExpressionAttributeValues={  # values defined in here will get injected to update expression
            ':positions': session.positions,
            ':data_imports': session.data_imports
        },
        ReturnValues="UPDATED_NEW"  # return the newly updated data point
    )
    return response


def delete_session(session_id: str):
    table = db.Table('Session')  # referencing to table Sessions
    response = table.delete_item(  # delete session using id
        Key={'session_id': session_id}
    )
    return response
