# Standard library imports
from typing import Union

# Third party imports
from pydantic import BaseModel


class UserGetDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    zip_code: str


class UserPutDto(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    phone: Union[str, None] = None
    email: Union[str, None] = None
    zip_code: Union[str, None] = None


class NamePutDto(BaseModel):
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


class ContactPutDto(BaseModel):
    phone: Union[str, None] = None
    email: Union[str, None] = None
    zip_code: Union[str, None] = None
