from pydantic import BaseModel
from typing import List, Optional, Any


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
