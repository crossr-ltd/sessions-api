from enum import Enum


class DatasetType(str, Enum):
    EXPERIMENTAL = "experimental"
    SET = "set"
    QUERY = "query"
