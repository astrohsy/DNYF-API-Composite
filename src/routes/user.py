# Standard library imports
from uuid import uuid4
from time import sleep

# Third party imports
from fastapi import APIRouter

# Local application imports
from src.core_microservice import UserMicroservice, ContactsMicroservice
from src.schema.user import UserGetDto, UserPostDto, UserPutDto, UserGetIdByEmailDto


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserGetDto)
def get_one_user(user_id: str):
    return UserMicroservice.get_user_info_id(user_id)


@router.put("/{user_id}", response_model=UserGetDto)
def update_user(user_id: str, updated_props: UserPutDto):
    # Use sleep() as a workaround to make sure that
    # core microservices have time to process requests

    UserMicroservice.update_name(user_id, updated_props)
    sleep(0.5)
    ContactsMicroservice.update_user_contacts(user_id, updated_props)
    sleep(0.5)

    return UserMicroservice.get_user_info_id(user_id)


@router.post("/", response_model=UserGetDto)
def create_user(props: UserPostDto):
    user_id = str(uuid4())

    # Use sleep() as a workaround to make sure that
    # core microservices have time to process requests
    UserMicroservice.create_user(user_id, props)
    sleep(0.5)
    ContactsMicroservice.create_user_contacts(user_id, props)
    sleep(0.5)

    return UserMicroservice.get_user_info_id(user_id)


@router.get("/{email}/id")
def lookup_user_id(email: str):
    return {"uid": ContactsMicroservice.get_user_id(email)}
