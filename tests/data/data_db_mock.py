from pathlib import Path

BASE_TESTS_DIR = Path(__file__).parent.parent
MEDIA_PATH = str(BASE_TESTS_DIR / "data/cat.jpeg")
MEDIAS_DIR = BASE_TESTS_DIR / "data/medias"


users_correct = [
    {"id": 1, "name": "Nick Ivanov", "api_key": "test"},
    {"id": 2, "name": "Ivan Petrov", "api_key": "dev"},
]

tweets_correct = [
    {
        "tweet_id": 1,
        "tweet_data": "Hello world!",
        "user_id": 1,
    },
    {
        "tweet_id": 2,
        "tweet_data": "How are you?",
        "user_id": 2,
    },
]

medias_correct = [
    {
        "media_id": 1,
        "media_path": MEDIA_PATH,
    },
    {
        "media_id": 2,
        "media_path": MEDIA_PATH,
    },
]
