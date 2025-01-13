from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt as jwt_auth
from core.config import auth_settings

user_data = {
    "user_id": str(uuid4()),
    "email": "service@cinema.io",
    "roles": ["service"],
}


def create_token(user_data):
    expires_time = datetime.now(tz=timezone.utc) + timedelta(seconds=86400 * 30 * 12)
    payload = {
        "user_id": user_data["user_id"],
        "email": user_data["email"],
        "roles": user_data["roles"],
        "exp": expires_time,
        "jti": str(uuid4()),
    }
    token = jwt_auth.encode(
        payload=payload,
        key=auth_settings.authjwt_secret_key,
        algorithm=auth_settings.authjwt_algorithm,
    )
    return token


if __name__ == "__main__":
    print(create_token(user_data))
