from fastapi import APIRouter

router = APIRouter()


@router.get("/api/users/me")
async def get_users_me():
    return {
        "result": True,
        "user": {
            "id": 1,
            "name": "John Doe",
            "followers": [
                {"id": 2, "name": "Alice"},
                {"id": 3, "name": "Bob"},
            ],
            "following": [
                {"id": 4, "name": "Charlie"},
                {"id": 5, "name": "Dave"},
            ],
        },
    }
