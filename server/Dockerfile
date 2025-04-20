FROM python:3.12.10-slim

WORKDIR /project

COPY ../pyproject.toml   ./
COPY ../poetry.lock      ./

RUN apt-get update

RUN pip install --upgrade pip wheel "poetry==2.1.2"

RUN poetry config virtualenvs.create false

RUN poetry install --only prod --no-root

COPY server/ ./server
WORKDIR /project/server

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]