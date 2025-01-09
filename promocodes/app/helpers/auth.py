import httpx
from core.config import promocodes_settings
from core.logger import logger
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

auth_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(auth_scheme),
):
    """
    Verify JWT token by requesting auth service, and having 'sender' role is mandatory.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    token = credentials.credentials

    logger.info(f"token: {token}")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{promocodes_settings.auth_service_url}?allow_roles={promocodes_settings.auth_sender_role}",
                headers={"Authorization": f"Bearer {token}"},
                timeout=promocodes_settings.auth_timeout,
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token {token}",
            )

        user_data = response.json()
        logger.info(f"user_data: {user_data}")

        return user_data

    except httpx.RequestError as exc:
        logger.error(f"Error connecting to auth service: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable",
        )
