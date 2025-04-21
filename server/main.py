import uvicorn
from fastapi import FastAPI

app = FastAPI()
PORT: int = 8000


@app.get("/api/hello/")
def hello_index():
    return {"message": "Hello World!!"}


if __name__ == "__main__":

    uvicorn.run(
        host="127.0.0.1",
        port=PORT,
        app="main:app",
        reload=True,
    )
