from typing import Sequence

from sqlalchemy import Result, select

from server.core.models import Users, db_helper

from .hashed_api_key import hash_api_key, validate_api_key


async def create_mock_data() -> None:
    """Создаёт тестовых пользователей, если их нет в базе"""

    mock_users = [
        {"name": "Ivan Volkov", "api_key": "test"},
        {"name": "Nikita Ivanov", "api_key": "dev"},
    ]

    async with db_helper.session_factory() as session:
        db_response: Result = await session.execute(select(Users))
        db_users: Sequence[Users] = db_response.scalars().all()

        if db_users:
            for mock_user in mock_users:
                user_exists = False

                for db_user in db_users:
                    if validate_api_key(
                        api_key=mock_user["api_key"],
                        hashed_api_key=db_user.api_key,
                    ):
                        user_exists = True
                        break

                if not user_exists:
                    hashed_api_key = hash_api_key(api_key=mock_user["api_key"])
                    user = Users(
                        name=mock_user["name"], api_key=hashed_api_key
                    )
                    session.add(user)
                    await session.commit()
        else:
            for mock_user in mock_users:
                hashed_api_key = hash_api_key(api_key=mock_user["api_key"])
                user = Users(name=mock_user["name"], api_key=hashed_api_key)
                session.add(user)
                await session.commit()
