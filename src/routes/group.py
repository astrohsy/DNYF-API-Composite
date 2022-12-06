"""
Group endpoint routing
"""
# Third party imports
from typing import Optional
from fastapi import APIRouter, Depends

from src.core_microservice import GroupsMicroservice

# Local application imports
from src.schema.group import (
    GroupGetDto,
    GroupGetDtoPaginated,
    GroupPostDto,
    GroupPostMemberDto,
    GroupPutDto,
)
from src.util.auth import get_oauth_userinfo, OAuthUserInfo


router = APIRouter(prefix="/groups", tags=["groups"])

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100


@router.get("/", response_model=GroupGetDtoPaginated)
def get_all_groups(
    offset: int = DEFAULT_OFFSET,
    limit: int = DEFAULT_LIMIT,
    group_name: Optional[str] = None,
    oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo),
):
    print(oauth_user_info)
    return GroupsMicroservice.get_all_groups(offset, limit, group_name)


@router.get("/{group_id}", response_model=GroupGetDto)
def get_one_group(
    group_id: int, oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo)
):
    return GroupsMicroservice.get_single_group(group_id)


@router.post("/", response_model=GroupGetDto)
def create_group(
    group: GroupPostDto, oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo)
):
    return GroupsMicroservice.create_group(group)


@router.put("/{group_id}", response_model=GroupGetDto)
def update_group(
    group_id: int,
    updated_props: GroupPutDto,
    oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo),
):
    return GroupsMicroservice.update_group(group_id, updated_props)


@router.delete("/{group_id}", status_code=204)
def delete_group(
    group_id: int, oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo)
):
    GroupsMicroservice.delete_group(group_id)


@router.post("/{group_id}/members", response_model=GroupGetDto)
def add_user_to_group(
    group_id: int,
    req_body: GroupPostMemberDto,
    oauth_user_info: OAuthUserInfo = Depends(get_oauth_userinfo),
):
    user_email = req_body.user_email

    return GroupsMicroservice.add_user_to_group(group_id, user_email)
