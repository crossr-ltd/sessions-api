from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from app.api.models.domains import Session, Position
from app.api.utils.db import get_db

from decimal import Decimal

db: ServiceResource = get_db()


def get_all_sessions():
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.scan()  # scan all data
    return response.get('Items', [])  # return data


def get_session(id: str):
    try:
        table = db.Table('Sessions')  # referencing to table Sessions
        response = table.get_item(Key={'id': id})  # get session using id (partition key)
        return response['Item']  # return single data
    except ClientError as e:
        raise ValueError(e.response['Error']['Message'])


def parse_position(position: Position):
    return dict(
        point_x=Decimal.from_float(position.point_x),
        point_y=Decimal.from_float(position.point_y),
        node_id=position.node_id)


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
            ':positions': [parse_position(position) for position in session.positions],
            ':data_imports': [dict(data_import) for data_import in session.data_imports]
        },
        ReturnValues="UPDATED_NEW"  # return the newly updated data point
    )
    return response


def delete_session(id: str):
    table = db.Table('Sessions')  # referencing to table Sessions
    response = table.delete_item(  # delete session using id
        Key={'id': id}
    )
    return response
