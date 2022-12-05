"""
Wrappers of core microservices.

TODO: Methods returning fake data to be replaced with actual calls to microservices
"""

# Standard library imports
import copy
from typing import List, Optional

# Third party imports
import requests

# Local application imports
from src.schema.group import (
    GroupGetDto,
    GroupGetDtoPaginated,
    GroupPostDto,
    GroupPutDto,
)
from src.schema.user import UserGetDto, ContactPutDto, NamePutDto, UserPostDto
from src.config import settings


# START FAKE DATA
next_group_id = 4

fake_group_data = [
    {
        "data": {
            "group_name": "OS Group",
            "group_capacity": 2,
            "group_id": 1,
            "links": [
                {
                    "href": "/groups/1",
                    "rel": "delete_group",
                    "type": "DELETE",
                },
            ],
        }
    },
    {
        "data": {
            "group_name": "ASE Group",
            "group_capacity": 4,
            "group_id": 2,
            "links": [
                {
                    "href": "/groups/2",
                    "rel": "delete_group",
                    "type": "DELETE",
                },
            ],
        }
    },
    {
        "data": {
            "group_name": "PLT Group",
            "group_capacity": 3,
            "group_id": 3,
            "links": [
                {
                    "href": "/groups/3",
                    "rel": "delete_group",
                    "type": "DELETE",
                },
            ],
        }
    },
]

fake_group_members = {
    "1": {
        "data": [
            {
                "member_id": "1",
            },
            {
                "member_id": "2",
            },
        ]
    },
    "2": {
        "data": [
            {
                "member_id": "2",
            },
            {
                "member_id": "3",
            },
        ]
    },
    "3": {
        "data": [
            {
                "member_id": "1",
            },
            {
                "member_id": "3",
            },
        ]
    },
}

fake_user_data = [
    {
        "data": {
            "uid": "sample1",
            "first_name": "A",
            "last_name": "A",
        }
    },
    {
        "data": {
            "uid": "sample2",
            "first_name": "B",
            "last_name": "B",
        }
    },
    {
        "data": {
            "uid": "sample3",
            "first_name": "C",
            "last_name": "C",
        }
    },
]

fake_contacts_data = [
    {
        "data": {
            "uid": "sample1",
            "email": "abc@abc",
            "phone": "123-456-789",
            "zip_code": "12345",
        }
    },
    {
        "data": {
            "uid": "sample2",
            "email": "qwe@qwe",
            "phone": "456-567-678",
            "zip_code": "45678",
        }
    },
    {
        "data": {
            "uid": "sample3",
            "email": "tyu@tyu",
            "phone": "234-345-125",
            "zip_code": "78906",
        }
    },
]
# END FAKE DATA


GROUP_MICROSERVICE_URL = settings.group_microservice_url

def get_user_info(user_id: str):
    """
    Helper function for returning user information from User and Contacts microservices
    """
    user_name = UserMicroservice.get_user_name(user_id)
    user_contacts = ContactsMicroservice.get_user_contacts(user_id)

    return {"id": user_id, **user_name, **user_contacts}


class GroupsMicroservice:
    @staticmethod
    def get_all_groups(
        offset: int, limit: int, group_name: Optional[str]
    ) -> GroupGetDtoPaginated:
        """
        TODO: replace with call to `GET groups/`
        TODO: pass through offset, limit, and search query parameters
        TODO: preserve pagination links returned from the Groups microservice
        """
        groups = []
        for group in fake_group_data:
            group_data = copy.deepcopy(group["data"])

            # Add group members
            group_data["members"] = GroupsMicroservice.get_group_members(
                group_data["group_id"]
            )

            fake_pagination_links = [
                {
                    "href": "...",
                    "rel": "get_next_group_page",
                    "type": "GET",
                },
                {
                    "href": "...",
                    "rel": "get_prev_group_page",
                    "type": "GET",
                },
            ]

            groups.append(group_data)

        return {"data": groups, "links": fake_pagination_links}

    @staticmethod
    def get_single_group(group_id: int) -> GroupGetDto:
        group = requests.get(f'{GROUP_MICROSERVICE_URL}/api/groups/{group_id}').json()

        # Add group members
        group["data"]["members"] = GroupsMicroservice.get_group_members(group_id)

        return group

    @staticmethod
    def get_group_members(group_id: int) -> List[UserGetDto]:
        members = requests.get(f'{GROUP_MICROSERVICE_URL}/api/groups/{group_id}/members').json()

        # Return members with name and contact info
        return [get_user_info(member["member_id"]) for member in members["data"]]

    @staticmethod
    def create_group(group: GroupPostDto) -> GroupGetDto:
        payload = {
            "group_name": group.group_name,
            "group_capacity": group.group_capacity,
        }

        res = requests.post(f'{GROUP_MICROSERVICE_URL}/api/groups/', json=payload).json()
        new_id = res["data"]["group_id"]

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(new_id)

    @staticmethod
    def update_group(group_id: int, updated_props: GroupPutDto) -> GroupGetDto:
        requests.put(
            f'{GROUP_MICROSERVICE_URL}/api/groups/{group_id}',
            json=updated_props.dict(exclude_none=True)
        )

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(group_id)

    @staticmethod
    def delete_group(group_id: int) -> None:
        requests.delete(f'{GROUP_MICROSERVICE_URL}/api/groups/{group_id}')

    @staticmethod
    def add_user_to_group(group_id: int, user_email: str) -> GroupGetDto:
        """
        TODO: replace with call to `POST groups/{group_id}/members`
        Note: the request body is {"member_id": 123}
        """

        user_id = ContactsMicroservice.get_user_id(user_email)

        fake_group_members[str(group_id)]["data"].append({"member_id": user_id})

        return GroupsMicroservice.get_single_group(group_id)


class UserMicroservice:
    @staticmethod
    def get_user_name(user_id: str):
        """
        TODO: replace with call to `GET /users/{id}`
        """
        user_data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_user_data)
        )[0]["data"]

        # Do it like this in case the User microservice returns more than just name
        name = {
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
        }

        return name

    @staticmethod
    def create_user(user_id: str, props: UserPostDto):
        """
        TODO: replace with call to `POST /users/{id}`
        """
        new_user = {
            "data": {
                "uid": user_id,
                "first_name": props.first_name,
                "last_name": props.last_name,
            }
        }

        fake_user_data.append(new_user)

    @staticmethod
    def get_user_info_id(user_id: str) -> UserGetDto:
        return get_user_info(user_id)

    @staticmethod
    def update_name(user_id: str, updated_props: NamePutDto) -> UserGetDto:
        """
        TODO: replace with call to `PUT /users/{id}`
        """
        user_data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_user_data)
        )[0]["data"]

        if updated_props.first_name is not None:
            user_data["first_name"] = updated_props.first_name

        if updated_props.last_name is not None:
            user_data["last_name"] = updated_props.last_name

        return UserMicroservice.get_user_info_id(user_id)


class ContactsMicroservice:
    @staticmethod
    def get_user_contacts(user_id: str):
        contacts = {
            "email": ContactsMicroservice.__get_user_email(user_id),
            "phone": ContactsMicroservice.__get_user_phone(user_id),
            "zip_code": ContactsMicroservice.__get_user_zipcode(user_id),
        }

        return contacts

    @staticmethod
    def create_user_contacts(user_id: str, props: UserPostDto):
        """
        TODO: replace with call to `POST /contacts/{id}`
        """
        new_contacts = {
            "data": {
                "uid": user_id,
                "email": props.email,
                "phone": props.phone,
                "zip_code": props.zip_code,
            }
        }

        fake_contacts_data.append(new_contacts)

    @staticmethod
    def update_user_contacts(user_id: str, updated_props: ContactPutDto) -> UserGetDto:

        ContactsMicroservice.__update_user_email(user_id, updated_props.email)
        ContactsMicroservice.__update_user_phone(user_id, updated_props.phone)
        ContactsMicroservice.__update_user_zipcode(user_id, updated_props.zip_code)

        return UserMicroservice.get_user_info_id(user_id)

    @staticmethod
    def get_user_id(user_email: str) -> str:
        """
        TODO: replace with call to `GET /contacts/{email}/id`
        """
        data = list(
            filter(lambda user: user["data"]["email"] == user_email, fake_contacts_data)
        )[0]["data"]

        return data["uid"]

    @staticmethod
    def __get_user_email(user_id: str) -> str:
        """
        TODO: replace with call to `GET /contacts/{id}/email`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["email"]

    @staticmethod
    def __update_user_email(user_id: str, email: str) -> None:
        """
        TODO: replace with call to `PUT /contacts/{id}/email`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        if email is not None:
            data["email"] = email

    @staticmethod
    def __get_user_phone(user_id: str) -> str:
        """
        TODO: replace with call to `GET /contacts/{id}/phone`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["phone"]

    @staticmethod
    def __update_user_phone(user_id: str, phone: str) -> None:
        """
        TODO: replace with call to `PUT /contacts/{id}/phone`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        if phone is not None:
            data["phone"] = phone

    @staticmethod
    def __get_user_zipcode(user_id: str) -> str:
        """
        TODO: replace with call to `GET /contacts/{id}/zip_code`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["zip_code"]

    @staticmethod
    def __update_user_zipcode(user_id: str, zip_code: str) -> None:
        """
        TODO: replace with call to `PUT /contacts/{id}/zip_code`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        if zip_code is not None:
            data["zip_code"] = zip_code
