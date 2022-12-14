"""
Wrappers of core microservices.
"""

# Standard library imports
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


GROUP_MICROSERVICE_URL = settings.group_microservice_url
USERS_MICROSERVICE_URL = settings.users_microservice_url
CONTACTS_MICROSERVICE_URL = settings.contacts_microservice_url

print(f"{GROUP_MICROSERVICE_URL=}")
print(f"{USERS_MICROSERVICE_URL=}")
print(f"{CONTACTS_MICROSERVICE_URL=}")


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
        query_params = {"offset": offset, "limit": limit, "group_name": group_name}
        res = requests.get(
            f"{GROUP_MICROSERVICE_URL}/api/groups/", params=query_params
        ).json()

        for group in res["data"]:
            # Add group members
            group["members"] = GroupsMicroservice.get_group_members(group["group_id"])

        return res

    @staticmethod
    def get_single_group(group_id: int) -> GroupGetDto:
        group = requests.get(f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}").json()

        # Add group members
        group["data"]["members"] = GroupsMicroservice.get_group_members(group_id)

        return group

    @staticmethod
    def get_group_members(group_id: int) -> List[UserGetDto]:
        members = requests.get(
            f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}/members"
        ).json()
        print(members)
        # Return members with name and contact info
        return [get_user_info(member["member_id"]) for member in members["data"]]

    @staticmethod
    def create_group(group: GroupPostDto) -> GroupGetDto:
        payload = {
            "group_name": group.group_name,
            "group_capacity": group.group_capacity,
        }

        res = requests.post(
            f"{GROUP_MICROSERVICE_URL}/api/groups/", json=payload
        ).json()
        new_id = res["data"]["group_id"]

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(new_id)

    @staticmethod
    def update_group(group_id: int, updated_props: GroupPutDto) -> GroupGetDto:
        requests.put(
            f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}",
            json=updated_props.dict(exclude_none=True),
        )

        # Call get_single_group as a shortcut for returning the proper schema
        return GroupsMicroservice.get_single_group(group_id)

    @staticmethod
    def delete_group(group_id: int) -> None:
        requests.delete(f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}")

    @staticmethod
    def add_user_to_group(group_id: int, user_email: str) -> GroupGetDto:
        user_id = ContactsMicroservice.get_user_id(user_email)

        requests.post(
            f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}/members",
            json={"member_id": user_id},
        )

        return GroupsMicroservice.get_single_group(group_id)

    @staticmethod
    def remove_user_from_group(group_id: int, user_email: str) -> GroupGetDto:
        user_id = ContactsMicroservice.get_user_id(user_email)

        requests.delete(
            f"{GROUP_MICROSERVICE_URL}/api/groups/{group_id}/members/{user_id}"
        )

        return GroupsMicroservice.get_single_group(group_id)


class UserMicroservice:
    @staticmethod
    def get_user_name(user_id: str):
        res = requests.get(f"{USERS_MICROSERVICE_URL}/users/{user_id}").json()

        # Do it like this in case the User microservice returns more than just name
        name = {
            "first_name": res["first_name"],
            "last_name": res["last_name"],
        }

        return name

    @staticmethod
    def create_user(user_id: str, props: UserPostDto):
        new_user = {
            "uid": user_id,
            "first_name": props.first_name,
            "last_name": props.last_name,
        }

        requests.post(
            f"{USERS_MICROSERVICE_URL}/users",
            json=new_user,
        )

    @staticmethod
    def get_user_info_id(user_id: str) -> UserGetDto:
        return get_user_info(user_id)

    @staticmethod
    def update_name(user_id: str, updated_props: NamePutDto) -> None:
        requests.put(
            f"{USERS_MICROSERVICE_URL}/users/{user_id}",
            json=updated_props.dict(exclude_none=True),
        )


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
        new_contacts = {
            "uid": user_id,
            "email": props.email,
            "phone_number": props.phone,
            "zip_code": props.zip_code,
        }

        res = requests.post(
            f"{CONTACTS_MICROSERVICE_URL}/contacts",
            json=new_contacts,
        )

        return res.status_code

    @staticmethod
    def update_user_contacts(user_id: str, updated_props: ContactPutDto) -> None:
        ContactsMicroservice.__update_user_email(user_id, updated_props.email)
        ContactsMicroservice.__update_user_phone(user_id, updated_props.phone)
        ContactsMicroservice.__update_user_zipcode(user_id, updated_props.zip_code)

    @staticmethod
    def get_user_id(user_email: str) -> str:
        payload = {"email": user_email}
        res = requests.get(
            f"{CONTACTS_MICROSERVICE_URL}/contacts/email/uid", json=payload
        ).json()

        return res["data"]["uid"]

    @staticmethod
    def __get_user_email(user_id: str) -> str:
        res = requests.get(f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/email")
        if res.status_code // 100 != 2:
            raise res.raise_for_status()

        return res.json()["data"]["email"]

    @staticmethod
    def __update_user_email(user_id: str, email: str) -> None:
        if email is not None:
            requests.put(
                f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/email",
                json={"email": email},
            )

    @staticmethod
    def __get_user_phone(user_id: str) -> str:
        res = requests.get(
            f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/phone"
        ).json()

        return res["data"]["phone_number"]

    @staticmethod
    def __update_user_phone(user_id: str, phone: str) -> None:
        if phone is not None:
            requests.put(
                f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/phone",
                json={"phone_number": phone},
            )

    @staticmethod
    def __get_user_zipcode(user_id: str) -> str:
        res = requests.get(f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/zip").json()

        return res["data"]["zip_code"]

    @staticmethod
    def __update_user_zipcode(user_id: str, zip_code: str) -> None:
        if zip_code is not None:
            requests.put(
                f"{CONTACTS_MICROSERVICE_URL}/contacts/{user_id}/zip",
                json={"zip_code": zip_code},
            )
