import pytest

from tests.data.data_db_mock import MEDIA_PATH, users_correct


@pytest.mark.asyncio
async def test_create_media_success(client, sample_media_jpg, db_session):
    """Тест успешного запроса к API
    POST /api/medias
    """

    user_api_key = users_correct[0]["api_key"]
    media_file = open(MEDIA_PATH, "rb")

    response = await client.post(
        "/api/medias",
        files={"file": media_file},
        headers={"api-key": user_api_key},
    )
    data = response.json()

    assert response.status_code == 201
    assert data["result"] is True
