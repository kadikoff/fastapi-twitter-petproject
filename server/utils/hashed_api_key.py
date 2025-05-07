import bcrypt


def hash_api_key(api_key: str) -> str:
    """Создаёт хэш api_key с генерацией соли"""

    salt = bcrypt.gensalt()
    api_key_bytes: bytes = api_key.encode()

    return bcrypt.hashpw(api_key_bytes, salt).decode()


def validate_api_key(api_key: str, hashed_api_key: str) -> bool:
    """Проверяет, соответствует ли api_key хэшу"""

    return bcrypt.checkpw(
        password=api_key.encode(),
        hashed_password=hashed_api_key.encode(),
    )
