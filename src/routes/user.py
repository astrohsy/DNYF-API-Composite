# Third party imports
from fastapi import APIRouter

# Local application imports
from src.core_microservice import UserMicroservice, ContactsMicroservice
from src.schema.user import UserGetDto, UserPutDto


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserGetDto)
def get_one_user(user_id: int):
    return UserMicroservice.get_user_info_id(user_id)


@router.put("/{user_id}", response_model=UserGetDto)
def update_user(user_id: int, updated_props: UserPutDto):
    UserMicroservice.update_name(user_id, updated_props)
    ContactsMicroservice.update_user_contacts(user_id, updated_props)

    return UserMicroservice.get_user_info_id(user_id)
