"""
Group endpoint routing
"""
# Third party imports
from fastapi import APIRouter, Request

# Local application imports
from ..schema.group import (
    GroupGetDto,
    GroupPostDto,
    GroupPutDto,
    GroupGetDtoPaginated,
    MemberGetDto,
    MemberPostDto,
)


router = APIRouter(prefix="/groups", tags=["groups"])

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100


@router.get("/", response_model=GroupGetDtoPaginated)
def read_groups(
    request: Request,
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
):
    raise NotImplementedError()


@router.get("/{group_id}", response_model=GroupGetDto)
def read_group(group_id: int):
    raise NotImplementedError()


@router.get("/{group_id}/members", response_model=MemberGetDto)
def get_members(
    group_id: int,
):
    raise NotImplementedError()


@router.post("/", response_model=GroupGetDto)
def create_group(group: GroupPostDto):
    raise NotImplementedError()


@router.post("/{group_id}/members", response_model=GroupGetDto)
def add_member_to_group(new_member: MemberPostDto, group_id: int):
    raise NotImplementedError()


@router.delete("/{group_id}", response_model=GroupGetDto)
def delete_group(group_id: int):
    raise NotImplementedError()


@router.delete("/{group_id}/members/{member_id}", response_model=GroupGetDto)
def delete_member(group_id: int, member_id: int):
    raise NotImplementedError()


@router.put("/{group_id}", response_model=GroupGetDto)
def edit_group(new_group: GroupPutDto, group_id: int):
    raise NotImplementedError()
