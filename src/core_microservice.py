"""
Wrappers of core microservices.

TODO: Methods returning fake data to be replaced with actual calls to microservices
"""

import copy
from typing import Optional


def get_user_info(user_id: int):
    """
    Helper function for returning user information from User and Contacts microservices
    """
    user_name = UserMicroservice.get_user_name(user_id)
    user_contacts = ContactsMicroservice.get_user_contacts(user_id)

    return {"id": user_id, **user_name, **user_contacts}


fake_groups_data = [
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
                "member_id": 1,
            },
            {
                "member_id": 2,
            },
        ]
    },
    "2": {
        "data": [
            {
                "member_id": 2,
            },
            {
                "member_id": 3,
            },
        ]
    },
    "3": {
        "data": [
            {
                "member_id": 1,
            },
            {
                "member_id": 3,
            },
        ]
    },
}


class GroupsMicroservice:
    @staticmethod
    def get_all_groups(offset: int, limit: int, group_name: Optional[str]):
        """
        TODO: replace with call to `GET groups/`
        TODO: pass through offset, limit, and search query parameters
        TODO: preserve pagination links returned from the Groups microservice
        """
        groups = []
        for group in fake_groups_data:
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
    def get_single_group(group_id: int):
        """
        TODO: replace with call to `GET groups/{group_id}`
        """
        group = list(
            filter(
                lambda group: group["data"]["group_id"] == group_id, fake_groups_data
            )
        )[0]
        group_copy = copy.deepcopy(group)

        # Add group members
        group_copy["data"]["members"] = GroupsMicroservice.get_group_members(group_id)

        return group_copy

    @staticmethod
    def get_group_members(group_id: int):
        """
        TODO: replace with call to `GET groups/{group_id}/members`
        """
        members = fake_group_members[str(group_id)]["data"]

        # Return members with name and contact info
        return [get_user_info(member["member_id"]) for member in members]


fake_user_data = [
    {
        "data": {
            "uid": 1,
            "first_name": "A",
            "last_name": "A",
        }
    },
    {
        "data": {
            "uid": 2,
            "first_name": "B",
            "last_name": "B",
        }
    },
    {
        "data": {
            "uid": 3,
            "first_name": "C",
            "last_name": "C",
        }
    },
]


class UserMicroservice:
    @staticmethod
    def get_user_name(user_id: int):
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


fake_contacts_data = [
    {
        "data": {
            "uid": 1,
            "email": "abc@abc",
            "phone": "123-456-789",
            "zip_code": "12345",
        }
    },
    {
        "data": {
            "uid": 2,
            "email": "qwe@qwe",
            "phone": "456-567-678",
            "zip_code": "45678",
        }
    },
    {
        "data": {
            "uid": 3,
            "email": "tyu@tyu",
            "phone": "234-345-125",
            "zip_code": "78906",
        }
    },
]


class ContactsMicroservice:
    @staticmethod
    def get_user_contacts(user_id: int):
        contacts = {
            "email": ContactsMicroservice.__get_user_email(user_id),
            "phone": ContactsMicroservice.__get_user_phone(user_id),
            "zip_code": ContactsMicroservice.__get_user_zipcode(user_id),
        }

        return contacts

    @staticmethod
    def __get_user_email(user_id: int):
        """
        TODO: replace with call to `GET /contacts/{id}/email`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["email"]

    @staticmethod
    def __get_user_phone(user_id: int):
        """
        TODO: replace with call to `GET /contacts/{id}/phone`
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["phone"]

    @staticmethod
    def __get_user_zipcode(user_id: int):
        """
        TODO: replace with call to `GET /contacts/{id}/zip_code` (?)
        """
        data = list(
            filter(lambda user: user["data"]["uid"] == user_id, fake_contacts_data)
        )[0]["data"]

        return data["zip_code"]