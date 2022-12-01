"""
Group endpoint routing
"""
# Third party imports
from typing import Optional
from fastapi import APIRouter

from src.core_microservice import GroupsMicroservice

# Local application imports
from src.schema.group import (
    GroupGetDto,
    GroupGetDtoPaginated,
    GroupPostDto,
    GroupPutDto,
)


router = APIRouter(prefix="/groups", tags=["groups"])

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100


@router.get("/", response_model=GroupGetDtoPaginated)
def get_all_groups(
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    group_name: Optional[str] = None,
):
    return GroupsMicroservice.get_all_groups(offset, limit, group_name)


@router.get("/{group_id}", response_model=GroupGetDto)
def get_one_group(group_id: int):
    return GroupsMicroservice.get_single_group(group_id)


@router.post("/", response_model=GroupGetDto)
def create_group(group: GroupPostDto):
    return GroupsMicroservice.create_group(group)


@router.put("/{group_id}", response_model=GroupGetDto)
def update_group(group_id: int, updated_props: GroupPutDto):
    return GroupsMicroservice.update_group(group_id, updated_props)


@router.delete("/{group_id}", status_code=204)
def delete_group(group_id: int):
    GroupsMicroservice.delete_group(group_id)
