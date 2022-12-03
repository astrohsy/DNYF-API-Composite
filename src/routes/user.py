# Local application imports
from uuid import uuid4

# Third party imports
from fastapi import APIRouter

# Local application imports
from src.core_microservice import UserMicroservice, ContactsMicroservice
from src.schema.user import UserGetDto, UserPostDto, UserPutDto


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserGetDto)
def get_one_user(user_id: str):
    return UserMicroservice.get_user_info_id(user_id)


@router.put("/{user_id}", response_model=UserGetDto)
def update_user(user_id: str, updated_props: UserPutDto):
    UserMicroservice.update_name(user_id, updated_props)
    ContactsMicroservice.update_user_contacts(user_id, updated_props)

    return UserMicroservice.get_user_info_id(user_id)


@router.post("/", response_model=UserGetDto)
def create_user(props: UserPostDto):
    user_id = str(uuid4())

    UserMicroservice.create_user(user_id, props)
    ContactsMicroservice.create_user_contacts(user_id, props)

    return UserMicroservice.get_user_info_id(user_id)
