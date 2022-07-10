import json
from decimal import Decimal
from typing import List

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from app.api.models.domains import Dataset, DatasetMetadata, DatasetRow
from app.api.services.datasets.utils import validate_dataset, get_fdr_values, get_mappings, get_mapping_metadata
from app.api.utils.db import get_db
from app.enums import DatasetType

db: ServiceResource = get_db()


def get_all_datasets():
    table = db.Table('Datasets')  # referencing to table Datasets
    response = table.scan()  # scan all data
    return response.get('Items', [])  # return data


def get_all_datasets_metadata(user_id):
    table = db.Table('Datasets')  # referencing to table Datasets
    response = table.scan()  # scan all data
    datasets = response.get('Items', [])
    # return [dataset.get('metadata', {}) for dataset in datasets if
    #         dataset.get('metadata', {}).get('user_id', '') == str(user_id)]
    return [dataset.get('metadata', {}) for dataset in datasets]


def get_dataset(id: str) -> Dataset:
    try:
        table = db.Table('Datasets')  # referencing to table Datasets
        response = table.get_item(Key={'id': id})  # get dataset using id (partition key)
        return response['Item']  # return single data
    except ClientError as e:
        raise ValueError(e.response['Error']['Message'])


def create_experimental_dataset(metadata: DatasetMetadata, rows: List[DatasetRow], perform_mapping: bool = True):
    dataset_valid, validation_errors = validate_dataset(metadata, rows, DatasetType.EXPERIMENTAL)
    if not dataset_valid:
        raise Exception("-".join(validation_errors))

    rows_with_fdr_value = get_fdr_values(rows)
    if perform_mapping:
        processed_rows, mapping_metadata = get_mappings(rows_with_fdr_value)
        metadata.mapping_metadata = mapping_metadata
    else:
        processed_rows = rows
        metadata.mapping_metadata = get_mapping_metadata(processed_rows)

    metadata.size = len([row for row in processed_rows if row.id is not None])
    metadata.node_types = list(set([row.type for row in rows if row.type is not None]))

    return Dataset(id=metadata.id, metadata=metadata, rows=processed_rows)


def create_set_dataset(metadata: DatasetMetadata, rows: List[DatasetRow], perform_mapping: bool = False):
    dataset_valid, validation_errors = validate_dataset(metadata, rows, DatasetType.SET)
    if not dataset_valid:
        raise Exception("-".join(validation_errors))

    if perform_mapping:
        rows_with_mappings, mapping_metadata = get_mappings(rows)
        metadata.mapping_metadata = mapping_metadata
        metadata.size = mapping_metadata.mapped_count
        metadata.node_types = list(set([row.mapping['type'] for row in rows if row.mapping['type'] is not None]))
        return Dataset(id=metadata.id, metadata=metadata, rows=rows_with_mappings)
    else:
        metadata.size = len(rows)
        metadata.node_types = list(set([row.node_type for row in rows if row.mapping['type'] is not None]))
        return Dataset(id=metadata.id, metadata=metadata, rows=rows)


def create_dataset(metadata: DatasetMetadata, rows: List[DatasetRow], perform_mapping: bool, return_dataset=True):
    if metadata.type == DatasetType.EXPERIMENTAL:
        print(perform_mapping)
        dataset = create_experimental_dataset(metadata, rows, perform_mapping)
    elif metadata.type == DatasetType.SET:
        dataset = create_set_dataset(metadata, rows, perform_mapping)
    elif metadata.type == DatasetType.QUERY:
        dataset = create_set_dataset(metadata, rows, perform_mapping)
    table = db.Table('Datasets')
    response = table.put_item(Item=json.loads(json.dumps(dataset.dict()), parse_float=Decimal))
    if return_dataset:
        return get_dataset(metadata.id)
    else:
        return response


def update_dataset_metadata(id: str, metadata: DatasetMetadata):
    table = db.Table('Datasets')  # referencing to table Sessions
    response = table.update_item(  # update single item
        Key={'id': id},  # using partition key specifying which attributes will get updated
        UpdateExpression="""                
            set
                metadata=:metadata
        """,
        ExpressionAttributeValues={  # values defined in here will get injected to update expression
            ':metadata': metadata.dict(),
        },
        ReturnValues="UPDATED_NEW"  # return the newly updated data point
    )
    return response


def delete_dataset(id: str):
    table = db.Table('Datasets')  # referencing to table Datasets
    response = table.delete_item(  # delete dataset using id
        Key={'id': id}
    )
    return response
