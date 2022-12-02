# Standard library imports
from typing import Union

# Local application imports
from src.schema.group import UserInfo


class UserGetDto(UserInfo):
    pass


class UserPostDto(UserInfo):
    pass


class UserPutDto(UserInfo):
    id: Union[int, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone: Union[str, None] = None
    email: Union[str, None] = None
    zip_code: Union[str, None] = None


class NamePutDto(UserInfo):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


class ContactPutDto(UserInfo):
    phone: Union[str, None] = None
    email: Union[str, None] = None
    zip_code: Union[str, None] = None
