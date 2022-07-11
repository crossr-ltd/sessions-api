import json
import os

import numpy as np
import logging
from typing import List, Tuple

import requests
from dotenv import load_dotenv

from app.api.models.domains import DatasetRow, DatasetMetadata, DatasetMappingMetadata, DatasetRowMapping
from app.enums import DatasetType

load_dotenv()


def validate_dataset(metadata: DatasetMetadata, rows: List[DatasetRow], dataset_type: DatasetType) -> Tuple[
    bool, List[str]]:
    validation_errors = []
    return len(validation_errors) == 0, validation_errors


def calculate_fdr_bh(p_values: List) -> List:
    """Benjamini-Hochberg p-value correction for multiple hypothesis testing."""
    p_values = np.asfarray(p_values)
    by_descend = p_values.argsort()[::-1]
    by_orig = by_descend.argsort()
    steps = float(len(p_values)) / np.arange(len(p_values), 0, -1)
    p_adjusted_values = np.minimum(1, np.minimum.accumulate(steps * p_values[by_descend]))
    return p_adjusted_values[by_orig]


def get_fdr_values(rows: List[DatasetRow]) -> List[DatasetRow]:
    rows_with_fdr: List[DatasetRow] = []
    calculated_fdr_values = calculate_fdr_bh([row.p_value for row in rows])

    for index, row in enumerate(rows):
        if row.fdr_value is not None:
            rows_with_fdr.append(row)
        elif row.p_value is None:
            logging.error(f'id: {row.id}/name: {row.name} has no sig level, skipping.')
            continue
        else:
            row.fdr_value = calculated_fdr_values[index]
            rows_with_fdr.append(row)

    return rows_with_fdr


def get_mapping_metadata(rows: List[DatasetRow]):
    return DatasetMappingMetadata(mapped_count=len([row for row in rows if row.id is not None]),
                                  not_mapped_count=len([row for row in rows if row.id is None]))


def find_duplicates(rows: List[DatasetRow]):
    # if using ID, remove ID duplicates.
    # if using name, use name duplicates.
    # if using both check for duplicates in both (this option for )
    row_ids = [row.source_id for row in rows]
    row_names = [row.source_name for row in rows]

    dupe_ids = [x for n, x in enumerate(row_ids) if x in row_ids[:n]]
    dupe_names = [x for n, x in enumerate(row_names) if x in row_names[:n]]

    dupe_name_ids = [row.source_id for row in rows if row.source_name in dupe_names]

    return list(set(dupe_ids + dupe_name_ids)), list(set(dupe_names))


def get_mappings(rows: List[DatasetRow]) -> List[DatasetRow]:
    mapping_input_data = dict(mapping_keys=["id", "name"],
                              mapping_values=[dict(id=row.source_id, name=row.source_name) for row in rows])

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'Authorization': f"Bearer {os.getenv('AUTH0_BEARER_TOKEN')}"}

    url = f"{os.getenv('KNOWLEDGE_GRAPH_API_URL')}/datasets/map-rows"
    data = json.dumps(dict(node_mappings_input=mapping_input_data))
    mapping_rows: List[DatasetRowMapping] = requests.post(url, headers=headers, data=data).json()

    duplicated_row_ids, duplicated_row_names = find_duplicates(rows)

    for i, row in enumerate(rows):
        row.mapping = mapping_rows[i]

        if (row.source_id is not None and row.source_id in duplicated_row_ids) or (
                row.source_name is not None and row.source_name in duplicated_row_names):
            row.mapping['duplicate'] = True
            continue

        row.id = row.mapping.get('id', None)
        row.name = row.mapping.get('name', None)
        row.type = row.mapping.get('type', None)

    return rows

