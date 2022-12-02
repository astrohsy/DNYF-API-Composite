"""
Wrappers of core microservices.

TODO: Methods returning fake data to be replaced with actual calls to microservices
"""

# Standard library imports
import copy
from typing import List, Optional

# Local application imports
from src.schema.group import (
    GroupGetDto,
    GroupGetDtoPaginated,
    GroupPostDto,
    GroupPutDto,
)
from src.schema.user import UserGetDto, ContactPutDto, NamePutDto, UserPostDto

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
            "uid": "1",
            "first_name": "A",
            "last_name": "A",
        }
    },
    {
        "data": {
            "uid": "2",
            "first_name": "B",
            "last_name": "B",
        }
    },
    {
        "data": {
            "uid": "3",
            "first_name": "C",
            "last_name": "C",
        }
    },
]

fake_contacts_data = [
    {
        "data": {
            "uid": "1",
            "email": "abc@abc",
            "phone": "123-456-789",
            "zip_code": "12345",
        }
    },
    {
        "data": {
            "uid": "2",
            "email": "qwe@qwe",
            "phone": "456-567-678",
            "zip_code": "45678",
        }
    },
    {
        "data": {
            "uid": "3",
            "email": "tyu@tyu",
            "phone": "234-345-125",
            "zip_code": "78906",
        }
    },
]
# END FAKE DATA


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
        """
        TODO: replace with call to `GET groups/{group_id}`
        """
        group = list(
            filter(lambda group: group["data"]["group_id"] == group_id, fake_group_data)
        )[0]
        group_copy = copy.deepcopy(group)

        # Add group members
        group_copy["data"]["members"] = GroupsMicroservice.get_group_members(group_id)

        return group_copy

    @staticmethod
    def get_group_members(group_id: int) -> List[UserGetDto]:
        """
        TODO: replace with call to `GET groups/{group_id}/members`
        """
        members = fake_group_members[str(group_id)]["data"]

        # Return members with name and contact info
        return [get_user_info(member["member_id"]) for member in members]

    @staticmethod
    def create_group(group: GroupPostDto) -> GroupGetDto:
        """
        TODO: replace with call to `POST groups/`
        """
        global next_group_id

        new_group = {
            "data": {
                "group_name": group.group_name,
                "group_capacity": group.group_capacity,
                "group_id": next_group_id,
                "links": [
                    {
                        "href": f"/groups/{next_group_id}",
                        "rel": "delete_group",
                        "type": "DELETE",
                    },
                ],
            }
        }

        fake_group_data.append(new_group)
        fake_group_members[str(next_group_id)] = {"data": []}

        next_group_id += 1

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(next_group_id - 1)

    @staticmethod
    def update_group(group_id: int, updated_props: GroupPutDto) -> GroupGetDto:
        """
        TODO: replace with call to `PUT groups/{group_id}`
        """
        curr_group = list(
            filter(lambda group: group["data"]["group_id"] == group_id, fake_group_data)
        )[0]

        if updated_props.group_capacity is not None:
            curr_group["data"]["group_capacity"] = updated_props.group_capacity

        if updated_props.group_name is not None:
            curr_group["data"]["group_name"] = updated_props.group_name

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(group_id)

    @staticmethod
    def delete_group(group_id: int) -> None:
        """
        TODO: replace with call to `DELETE groups/{group_id}`
        """
        global fake_group_data

        fake_group_data = list(
            filter(lambda group: group["data"]["group_id"] != group_id, fake_group_data)
        )


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
