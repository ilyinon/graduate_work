import httpx
import jwt
from core.config import purchase_settings


async def check_from_auth(
    credentials: str,
) -> bool:
    # return True
    if credentials:
        token = credentials.credentials
        headers = {"Authorization": f"Bearer {token}"}
        params = {}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                purchase_settings.auth_server_url, headers=headers, params=params
            )
            if response.status_code == 200:
                return True
    return False


async def take_user_id(jwt_token: str) -> str:
    payload = jwt.decode(jwt_token, options={"verify_signature": False})
    return payload.get("user_id")
