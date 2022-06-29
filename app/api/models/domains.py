from enum import Enum
from uuid import uuid4
from pydantic import Field
from decimal import Decimal
from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional, Any

from decimal import Decimal


class Position(BaseModel):
    node_id: str
    point_x: Decimal
    point_y: Decimal


class DataImportType(str, Enum):
    SET = "Set",
    OBSERVATION = "Observation",
    QUERY = "Query"


class DataImport(BaseModel):
    id: str
    name: str
    type: DataImportType
    nodes: List
    metadata: Any
    color: str


class SessionMetadata(BaseModel):
    id: str
    user_id: str
    name: str
    creation_date: str
    description: Optional[str]


class Session(BaseModel):
    id: str
    metadata: SessionMetadata
    positions: Optional[List[Position]]
    data_imports: Optional[List[DataImport]]
