import logging
import socket

from sqlalchemy import select

from server.core.models import Users, db_helper


async def create_mock_data() -> None:
    """Создаёт тестовых пользователей, если их нет в базе"""

    user_1 = Users(name="Ivan Volkov", api_key="test")
    user_2 = Users(name="Nikita Ivanov", api_key="dev")

    try:
        async with db_helper.session_factory() as session:
            test_user = await session.execute(
                select(Users).where(Users.api_key == user_1.api_key)
            )
            if not test_user.scalar():
                session.add(user_1)

            dev_user = await session.execute(
                select(Users).where(Users.api_key == user_2.api_key)
            )
            if not dev_user.scalar():
                session.add(user_2)

            await session.commit()
    except socket.gaierror as exc:
        logging.error(
            "Ошибка: тестовыe данные пользователей не добавлены! "
            "Возможно отсутствует подключение к базе данных!\n\n%s",
            str(exc),
        )
