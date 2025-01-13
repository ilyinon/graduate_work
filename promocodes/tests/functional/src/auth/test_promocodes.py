import http

import pytest
from faker import Faker
from tests.functional.settings import test_settings

fake = Faker()
pytestmark = pytest.mark.asyncio

url_template = "{service_url}/api/v1/promocodes/{endpoint}"
headers = {"Content-Type": "application/json"}


url_validate = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="validate"
)
url_list = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="list"
)
url_apply = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="apply"
)
url_revoke = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="revoke"
)
url_generate = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="generate"
)
url_assign = url_template.format(
    service_url=test_settings.promocodes_dsn, endpoint="assign"
)


auth_url_template = "{service_url}/api/v1/auth/{endpoint}"
user_url_template = "{service_url}/api/v1/users/{endpoint}"

headers = {"Content-Type": "application/json"}


url_signup = auth_url_template.format(
    service_url=test_settings.app_dsn, endpoint="signup"
)
url_login = auth_url_template.format(
    service_url=test_settings.app_dsn, endpoint="login"
)
url_user_profile = user_url_template.format(
    service_url=test_settings.app_dsn, endpoint=""
)


auth_headers = {"Authorization": f"Bearer {test_settings.promocode_service_token}"}
WORK_PROMOCODE = "MINUS100"
NOT_WORK_PROMOCODE = "999MINUS999"
working_generate = {
    "discount_percent": 0,
    "discount_rubles": 333,
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "usage_limit": 0,
    "is_active": "true",
    "is_one_time": "false",
}

not_working_generate = {
    "start_date": "2025-01-01",
    "end_date": "2025-12-31",
    "usage_limit": 0,
    "is_active": "true",
    "is_one_time": "false",
}

user = {
    "email": fake.email(),
    "password": fake.password(),
    "full_name": fake.name(),
    "username": fake.simple_profile()["username"],
}


async def test_validate_promocode(session):
    async with session.get(
        f"{url_validate}/{WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body == {
            "promocode": "MINUS100",
            "discount_percent": 0,
            "discount_rubles": 100,
        }


async def test_invalid_promocode(session):
    async with session.get(
        f"{url_validate}/{NOT_WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        await response.json()
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_list_promocodes(session):
    async with session.get(url_list, headers=auth_headers) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        promocode_id = body[0]["id"]
        # assert len(body) == 3


async def test_apply_promocode(session):
    async with session.post(
        f"{url_apply}/{WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK


async def test_apply_invalid_promocode(session):
    async with session.post(
        f"{url_apply}/{NOT_WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_revoke_promocode(session):
    async with session.post(
        f"{url_revoke}/{WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK


async def test_revoke_invalid_promocode(session):
    async with session.post(
        f"{url_revoke}/{NOT_WORK_PROMOCODE}", headers=auth_headers
    ) as response:
        await response.json()
        assert response.status == http.HTTPStatus.NOT_FOUND


async def test_generate_promocode(session):
    async with session.post(
        f"{url_generate}", headers=auth_headers, json=working_generate
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.OK
        assert body["is_active"] == True
        assert body["discount_rubles"] == 333
        assert body["discount_percent"] == 0
        assert body["is_one_time"] == False
        assert body["usage_limit"] == 0


async def test_invalid_generate_promocode(session):
    async with session.post(
        f"{url_generate}", headers=auth_headers, json=not_working_generate
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.UNPROCESSABLE_ENTITY


async def test_assign_promocode(session):
    async with session.post(url_signup, json=user) as response:
        await response.json()

    async with session.post(url_login, json=user) as response:
        body = await response.json()
        access_token = body["access_token"]

    async with session.get(
        url_user_profile, headers={"Authorization": f"Bearer {access_token}"}
    ) as response:
        body = await response.json()
        user_email = body["email"]

    async with session.get(url_list, headers=auth_headers) as response:
        body = await response.json()
        promocode_name = body[0]["promocode"]

    assign_promocode = {"user_email": user_email, "promocode": promocode_name}

    async with session.post(
        f"{url_assign}", headers=auth_headers, json=assign_promocode
    ) as response:
        body = await response.json()
        assert response.status == http.HTTPStatus.NOT_FOUND
        # The problem is to use the same Auth DB where user is present
