

from fastapi import APIRouter, Request

from app.api.models.schemas import DatasetCreateParams, DatasetUpdateMetadataParams
from app.api.services.datasets.datasets import get_dataset, create_dataset, delete_dataset, \
    get_all_datasets_metadata, update_dataset_metadata

router = APIRouter()


@router.get("/{id}")
async def dataset_get(request: Request, id: str):
    return get_dataset(id)


@router.post("/update/metadata")
async def dataset_update_metadata(request: Request, dataset_update_metadata_params: DatasetUpdateMetadataParams):
    return update_dataset_metadata(**dict(dataset_update_metadata_params))


@router.get('/{id}/delete')
async def dataset_delete(request: Request, id: str):
    return delete_dataset(id)


@router.get("")
async def dataset_get_all_metadata(request: Request):
    return get_all_datasets_metadata(user_id=request.state.user_id)


@router.post("/create")
async def dataset_create(request: Request, dataset_create_params: DatasetCreateParams):
    return create_dataset(**dict(dataset_create_params))
