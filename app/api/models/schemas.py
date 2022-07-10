from typing import List

from pydantic import BaseModel

from app.api.models.domains import Session, DatasetMetadata, DatasetRow


class SessionUpdateParams(BaseModel):
    session: Session


class SessionCreateParams(BaseModel):
    session: Session


class DatasetUpdateParams(BaseModel):
    metadata: DatasetMetadata


class DatasetCreateParams(BaseModel):
    metadata: DatasetMetadata
    rows: List[DatasetRow]
    perform_mapping: bool = True


class DatasetUpdateMetadataParams(BaseModel):
    id: str
    metadata: DatasetMetadata
