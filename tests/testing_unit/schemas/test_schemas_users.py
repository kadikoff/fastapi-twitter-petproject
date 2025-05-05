import pytest
from pydantic import ValidationError

from server.api.crud import crud_users
from server.core.models import Users
from server.core.schemas.schemas_users import UserRead
from tests.data.data_db_for_tests import user_data_invalid


@pytest.mark.asyncio
async def test_user_read_success(db_session):
    """Тест успешной валидации данных
    по схеме UserRead с использованием валидных данных
    """

    user: Users = await crud_users.get_user_by_id(
        session=db_session, user_id=1
    )
    assert user is not None

    user_data = {"user": user}
    user_read = UserRead.model_validate(user_data, from_attributes=True)

    assert user_read
    assert isinstance(user_read, UserRead)
    assert user_read.result
    assert user_read.user.id == user.id
    assert user_read.user.name == user.name


def test_user_read_invalid_error():
    """Тест обработки ошибки при валидации
    данных по схеме UserRead с использованием
    невалидных данных
    """

    with pytest.raises(ValidationError) as exc_info:
        UserRead(**user_data_invalid)

    errors = exc_info.value.errors()
    assert len(errors) == 3

    assert errors[0]["loc"] == ("user", "id")
    assert errors[0]["type"] == "int_type"
    assert "Input should be a valid integer" in errors[0]["msg"]

    assert errors[1]["loc"] == ("user", "followers")
    assert errors[1]["type"] == "list_type"

    assert errors[2]["loc"] == ("user", "following")
    assert errors[2]["type"] == "list_type"
