user_data_invalid = {
    "result": "true",
    "user": {
        "id": [],
        "name": "Aleksey Owner",
        "followers": {"id": 2, "name": "Nikita Ivanov"},
        "following": {"id": 3, "name": "Ivan Volkov"},
    },
}

tweet_no_media_valid = {
    "tweet_data": "Tweet without media!",
    "tweet_media_ids": [],
}

tweet_media_valid = {
    "tweet_data": "Tweet with media!",
    "tweet_media_ids": [1],
}

tweet_no_data_invalid = {
    "tweet_data": "",
    "tweet_media_ids": [],
}
