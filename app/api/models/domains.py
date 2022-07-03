from pydantic import BaseModel
from typing import List, Optional, Any

from app.enums import DatasetType


class DatasetMappingMetadata(BaseModel):
    mapped_count: int
    not_mapped_count: int


class DatasetMetadata(BaseModel):
    id: str
    name: str
    type: DatasetType
    date: str
    user_id: Optional[str]
    description: Optional[str]
    primary_quantification_key: Optional[str]
    primary_category_key: Optional[str]
    other_categories_keys: Optional[List[str]]
    mapping_metadata: Optional[DatasetMappingMetadata]
    query: Optional[Any]


class DatasetRowMapping(BaseModel):
    mapped: bool
    id: Optional[str]
    name: Optional[str]
    type: Optional[str]


class DatasetRow(BaseModel):
    id: Optional[str]
    name: Optional[str]
    node_type: Optional[str]
    primary_quantification_value: Optional[float]
    p_value: Optional[float]
    fdr_value: Optional[float]
    primary_category_value: Optional[str]
    other_categories: Optional[List[dict]]
    mapping: Optional[DatasetRowMapping]


class Dataset(BaseModel):
    id: str
    metadata: DatasetMetadata
    rows: List[DatasetRow]


class SessionMetadata(BaseModel):
    id: str
    user_id: str
    name: str
    creation_date: str
    description: Optional[str]


class Session(BaseModel):
    id: str
    metadata: SessionMetadata
    positions: Optional[List[Any]]
    dataImports: Optional[List[Any]]
    styles: List[Any]
    analysisReadouts: List[Any]
    filters: List[Any]
    subgraphWithMetadata: Any
    hiddenNodes: List[Any]
