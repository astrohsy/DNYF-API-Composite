# Standard library imports
from enum import Enum

# Third party imports
from pydantic import BaseModel
from typing import List, Union


class HTTPMethod(str, Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    delete = "DELETE"


class Link(BaseModel):
    """Link properties."""

    href: str
    rel: str
    type: HTTPMethod


class DeleteGroupLink(Link):
    href: str
    rel = "delete_group"
    type = HTTPMethod.get


class NextPageLink(Link):
    href: str
    rel = "get_next_group_page"
    type = HTTPMethod.get


class PrevPageLink(Link):
    href: str
    rel = "get_prev_group_page"
    type = HTTPMethod.get


class UserInfo(BaseModel):
    """User properties"""

    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    zip_code: str


class GroupBaseDto(BaseModel):
    """Shared group properties."""

    group_name: str
    group_capacity: int


class GroupDto(GroupBaseDto):
    """Group properties with links."""

    group_id: int
    members: List[UserInfo]
    links: List[Union[DeleteGroupLink, None]]


class GroupPostDto(GroupBaseDto):
    """Group properties for creating a new group."""

    pass


class GroupPutDto(GroupBaseDto):
    """Group properties for updating a group."""

    group_name: Union[str, None] = None
    group_capacity: Union[int, None] = None


class GroupGetDto(BaseModel):
    """Group properties to return to client."""

    data: GroupDto


class GroupGetDtoPaginated(BaseModel):
    """Group properties to return to client with pagination."""

    data: List[GroupDto]
    links: List[Union[NextPageLink, PrevPageLink]]
