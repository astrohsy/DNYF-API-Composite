from typing import Optional
from fastapi import APIRouter

from src.core_microservice import UserMicroservice

router = APIRouter(prefix="/users")

DEFAULT_OFFSET = 0
DEFAULT_LIMIT = 100

from src.schema.group import (
    UserInfo  
)

@router.get("/{user_id}", response_model=UserInfo)
def get_one_user(user_id: int):
    return UserMicroservice.get_user_info_id(user_id)