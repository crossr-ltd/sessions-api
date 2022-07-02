import json
from decimal import Decimal
from typing import List

from boto3.resources.base import ServiceResource
from botocore.exceptions import ClientError

from app.api.models.domains import Dataset, DatasetMetadata, DatasetRow
from app.api.services.datasets.utils import validate_dataset, get_fdr_values, get_mappings
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
    return [dataset.get('metadata', {}) for dataset in datasets if
            dataset.get('metadata', {}).get('user_id', '') == str(user_id)]


def get_dataset(id: str) -> Dataset:
    try:
        table = db.Table('Datasets')  # referencing to table Datasets
        response = table.get_item(Key={'id': id})  # get dataset using id (partition key)
        return response['Item']  # return single data
    except ClientError as e:
        raise ValueError(e.response['Error']['Message'])


def create_experimental_dataset(metadata: DatasetMetadata, rows: List[DatasetRow]):
    dataset_valid, validation_errors = validate_dataset(metadata, rows, DatasetType.EXPERIMENTAL)
    if not dataset_valid:
        raise Exception("-".join(validation_errors))

    rows_with_fdr_value = get_fdr_values(rows)
    rows_with_mappings, mapping_metadata = get_mappings(rows_with_fdr_value)
    metadata.mapping_metadata = mapping_metadata
    return Dataset(id=metadata.id, metadata=metadata, rows=rows_with_mappings)


def create_set_dataset(metadata: DatasetMetadata, rows: List[DatasetRow]):



def create_dataset(metadata: DatasetMetadata, rows: List[DatasetRow]):
    # any initial validation.
    if metadata.type == DatasetType.EXPERIMENTAL:
        dataset = create_experimental_dataset(metadata, rows)
    else:
        raise NotImplementedError()
    table = db.Table('Datasets')
    response = table.put_item(Item=json.loads(json.dumps(dataset.dict()), parse_float=Decimal))
    return response


def delete_dataset(id: str):
    table = db.Table('Datasets')  # referencing to table Datasets
    response = table.delete_item(  # delete dataset using id
        Key={'id': id}
    )
    return response
