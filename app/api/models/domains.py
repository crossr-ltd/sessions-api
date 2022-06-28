from enum import Enum
from uuid import uuid4
from pydantic import Field
from decimal import Decimal
from pydantic import BaseModel
from pydantic.types import UUID4
from typing import List, Optional, Any


class Position(BaseModel):
    node_id: str
    point_x: float
    point_y: float


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


class Session(BaseModel):
    id: str
    user_id: str
    positions: Optional[List[Position]]
    data_imports: Optional[List[DataImport]]
