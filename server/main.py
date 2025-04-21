import uvicorn
from fastapi import FastAPI

app = FastAPI()
PORT: int = 8000


@app.get("/api/hello/")
def hello_index():
    return {"message": "Hello World!"}


# @app.get("/api/users/me")
# def get_my_profile():
#     return {
#         "result": True,
#         "user": {
#             "id": 1,
#             "name": "John Doe",
#             "followers": [
#                 {"id": 2, "name": "Alice"},
#                 {"id": 3, "name": "Bob"}
#             ],
#             "following": [
#                 {"id": 4, "name": "Charlie"},
#                 {"id": 5, "name": "Dave"}
#             ]
#         }
#     }


if __name__ == "__main__":

    uvicorn.run(
        host="127.0.0.1",
        port=PORT,
        app="main:app",
        reload=True,
    )
