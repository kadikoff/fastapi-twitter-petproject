## Описание проекта
Реализация API backend-части клона Twitter с использованием следующих технологий:
- Дизайн REST API
- Реализация на FastAPI (ASGI Uvicorn)
- Nginx для отдачи статических файлов и проксировании на backend
- Работа с PostgreSQL через SQLAlchemy
- Миграции с Alembic
- Валидация через Pydantic-схемы
- Полное покрытие unit-тестами
- Pre-commit с хуками на линтеры 
- CI с проверкой кода линтерами и тестами
- Докеризацию и развертывание через Docker Compose

### Функционал приложения

Пользователь будет переходить на сайт уже имея у себя ключ
для авторизации (test). Все
endpoint имеют `http-header` с названием `api-key`. Вот сюда frontend
будет подставлять его. На стороне фронтенда разработана небольшая форма, в которую можно
подставить ключ для пользователя на бэкенде. 

При развертывании проекта в базе данных уже будут находиться два пользователя с ключами `test` и `dev` - используя эти ключи, 
будет доступен полный функционал приложения, подробнее о нём:
- Пользователь может добавить новый твит
- Пользователь может удалить свой твит
- Пользователь может зафоловить другого пользователя
- Пользователь может отписаться от другого пользователя
- Пользователь может отмечать твит как понравившийся
- Пользователь может убрать отметку «Нравится»
- Пользователь может получить ленту из твитов отсортированных в
порядке убывания по популярности от пользователей, которых он
фоловит
- Твит может содержать картинку

### Зависимости проекта (production)

- `fastapi==0.115.12` - Современный веб-фреймворк для создания API с автоматической генерацией документации 
- `uvicorn==0.34.2` - ASGI-сервер для запуска FastAPI приложения с поддержкой асинхронности
- `orjson==3.10.18` - Быстрый JSON-сериализатор/десериализатор (альтернатива стандартному json)
- `bcrypt==4.3.0"` - хэширование api-key
- `pydantic==2.7.0` - Библиотека для валидации данных и создания моделей с аннотацией типов
- `pydantic-settings==2.9.1` - Расширение Pydantic для работы с конфигурацией приложения
- `alembic==1.15.2` - Инструмент для миграций базы данных 
- `sqlalchemy[asyncio]==2.0.20` - ORM с поддержкой асинхронных запросов к PostgreSQL
- `asyncpg==0.30.0` - Асинхронный драйвер PostgreSQL для Python
- `aiofiles==24.1.0` - Асинхронная работа с файлами (используется для загрузки медиа)
- `python-multipart==0.0.20` - Обработка multipart/form-data (нужно для загрузки файлов через FastAPI)

## Быстрый старт

### Предварительные требования (наличие на пк)
- **ОС**: Unix-подобная система (Linux/Ubuntu/macOS)
- **Git** (система контроля версий)
- **Docker** и **Docker compose**


### Установка и запуск
1. Склонируйте репозиторий:
   
   ```
   git clone https://github.com/kadikoff/fastapi-twitter-petproject.git
2. Создайте и настройте `.env` файл по аналогии с `.example.env`. Ниже приведен примёр переменных, которые можно изменить:

   ```env
   DB_USER=test
   DB_PASS=test
   DB_NAME=test
3. Разверните проект через Docker Compose
   
   ```
   docker compose up --build
4. Перейдите в браузер по ссылке
   
   ```
   http://localhost:8080/

## Структура проекта

```
twitter-clone/  
├── alembic/                      # Миграции базы данных  
├── client/                       # Client - фронтенд и nginx
│   ├── static/                   # Фронтенд  
│   ├── Dockerfile                # Конфигурация Docker для статики  
│   └── nginx.conf                # Конфигурация Nginx  
├── server/                       # Server - основной backend-модуль  
│   ├── api/                      # API endpoints  
│   │   ├── crud/                 # CRUD функции  
│   │   └── routes/               # Маршруты FastAPI  
│   ├── core/                     # Ядро приложения  
│   │   ├── dependencies/         # Зависимости  
│   │   ├── middlewares/          # Промежуточное ПО  
│   │   ├── models/               # Модели базы данных  
│   │   ├── schemas/              # Pydantic схемы
│   │   └── config.py             # Конфигурационный файл проекта
│   ├── medias/                   # Директория для хранения медиафайлов
│   ├── utils/                    # Вспомогательные утилиты  
│   ├── create_app.py             # Фабрика приложения  
│   ├── Dockerfile                # Конфигурация Docker для backend 
│   ├── error_handlers.py         # Обработчики ошибок  
│   └── main.py                   # Точка входа  
├── tests/                        # Тесты
│   ├── data/                     # Данные для тестов  
│   ├── testing_unit/             # Юнит-тесты
│   │   ├── schemas/              # Тестирование pydantic-схем
│   │   └── utils/                # Тестирование утилит 
│   ├── testing_integration/      # Интеграционные тесты  
│   │   ├── crud/                 # Тестирование crud функций
│   │   └── database/             # Тестирование создания бд
│   └── testing_system/           # Системные тесты  
│       └── routes/               # Тестирование маршрутов FastAPI
├── .example.env                  # Шаблон .env файла  
├── .flake8                       # Конфигурация линтера  
├── .gitignore                    # Игнорируемые файлы Git  
├── .gitlab-ci.yml                # CI/CD конфигурация  
├── .pre-commit-config.yaml       # Настройки pre-commit  
├── alembic.ini                   # Конфигурация Alembic  
├── docker-compose.yml            # Конфигурация Docker Compose  
├── poetry.lock                   # Фиксация версий зависимостей  
├── pyproject.toml                # Конфигурация проекта  
└── README.md                     # Документация проекта
```

## Тестирование приложения
### Предварительные требования (наличие на пк)
- **ОС**: Unix-подобная система (Linux/Ubuntu/macOS)
- **Git** (система контроля версий)
- **Python** версии 3.12 или выше
- **PyCharm** (рекомендуемая IDE)
- **Poetry** (менеджер зависимостей)

### Установка Poetry
1. Загрузите и установите Poetry через терминал:
    
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
2. Добавьте Poetry в переменные окружения. Откройте файл .bashrc, в терминале введите:

   ```bash
   nano ~/.bashrc
   ```

   Вставьте в конец файла:
   
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```

   Сохраните изменения: `Ctr + X` > `Y` > `Enter`
3. Обновите настройки терминала:

   ```bash
   source ~/.bashrc
   ```


### Установка и настройка проекта
1. Склонируйте репозиторий:
   
   ```
   git clone https://github.com/kadikoff/fastapi-twitter-petproject.git
2. Создайте и настройте `.env` файл по аналогии с `.example.env`. Ниже приведен примёр переменных, которые можно изменить:

   ```env
   DB_USER=test
   DB_PASS=test
   DB_NAME=test
### Установка зависимостей и активация виртуального окружения
1. Установите зависимости. Откройте проект через IDE Pycharm и в терминале введите:

   ```bash
   poetry install --only dev

2. Добавьте новый интерпретатор в Pycharm. В правом нижнем углу IDE нажмите `Add New Interpreter` > `Add Local Interpreter`, задайте следующие настройки:
   - **Environment**: Generate new
   - **Type**: Poetry
   - **Base python**: Python 3.12.*
   - **Path to poetry**: /home/user/.local/bin/poetry
4. Для получения команды, активирующей виртуальное окружение, введите:
   ```bash
   poetry env activate
5. Введите в терминале то, что он выдал из предыдущего пункта, **пример**:
   ```bash
   source /home/user/.cache/pypoetry/virtualenvs/twitter-social-network-7uC99hQJ-py3.12/bin/activate
   ```

После всех установок и настроек перейдите к тестированию приложения - об этом написано далее.  
Для деактивации виртуального окружения введите `deactivate`.

---

### Использование pre-commit (линтеров)
- Для проверки кода линтерами используйте команду:

  ```bash
  pre-commit run --all-files
  ```

### Использование pytest
- Для тестирования приожения используйте команду:
  
  ```bash
  pytest -v ./tests
  ```
- Для вывод отчёта о покрытии приложения тестами введите:
  
   ```bash
   pytest --cov=./server
   ```
**Таблица с отчётом о покрытии тестами**  
**Общее покрытие:** 87% (530 строк кода, 67 пропущено)

| Файл                                          | Строк | Пропущено | Покрытие |
|-----------------------------------------------|:-----:|:----:|:-----:|
| `server/__init__.py`                          |   0   |  0   | 100%  |
| `server/api/__init__.py`                      |   0   |  0   | 100%  |
| `server/api/crud/__init__.py`                 |   0   |  0   | 100%  |
| `server/api/crud/crud_likes.py`               |  17   |  0   | 100%  |
| `server/api/crud/crud_medias.py`              |  16   |  0   | 100%  |
| `server/api/crud/crud_tweets.py`              |  44   |  5   | 89%   |
| `server/api/crud/crud_users.py`               |  30   |  0   | 100%  |
| `server/api/routes/__init__.py`               |   8   |  0   | 100%  |
| `server/api/routes/routes_medias.py`          |  13   |  1   | 92%   |
| `server/api/routes/routes_tweets.py`          |  31   |  5   | 84%   |
| `server/api/routes/routes_users.py`           |  25   |  4   | 84%   |
| `server/core/__init__.py`                     |   0   |  0   | 100%  |
| `server/core/config.py`                       |  47   |  1   | 98%   |
| `server/core/dependencies/__init__.py`        |   0   |  0   | 100%  |
| `server/core/dependencies/authenticate.py`    |  10   |  2   | 80%   |
| `server/core/middlewares/__init__.py`         |   4   |  0   | 100%  |
| `server/core/middlewares/log_new_request.py`  |   7   |  0   | 100%  |
| `server/core/models/__init__.py`              |   7   |  0   | 100%  |
| `server/core/models/db_helper.py`             |  12   |  3   | 75%   |
| `server/core/models/model_base.py`            |   3   |  0   | 100%  |
| `server/core/models/model_likes.py`           |  17   |  3   | 82%   |
| `server/core/models/model_medias.py`          |  14   |  2   | 86%   |
| `server/core/models/model_tweets.py`          |  18   |  4   | 78%   |
| `server/core/models/model_users.py`           |  19   |  3   | 84%   |
| `server/core/schemas/__init__.py`             |   0   |  0   | 100%  |
| `server/core/schemas/schemas_base.py`         |  24   |  0   | 100%  |
| `server/core/schemas/schemas_likes.py`        |   9   |  1   | 89%   |
| `server/core/schemas/schemas_medias.py`       |   4   |  0   | 100%  |
| `server/core/schemas/schemas_tweets.py`       |  23   |  0   | 100%  |
| `server/core/schemas/schemas_users.py`        |  10   |  0   | 100%  |
| `server/create_app.py`                        |  23   |  3   | 87%   |
| `server/error_handlers.py`                    |  18   |  2   | 89%   |
| `server/main.py`                              |   6   |  1   | 83%   |
| `server/utils/__init__.py`                    |   0   |  0   | 100%  |
| `server/utils/create_mock_data.py`            |  26   |  21  | 19%   |
| `server/utils/hashed_api_key.py`              |   7   |  0   | 100%  |
| `server/utils/media_writer.py`                |  38   |  6   | 84%   |
| **TOTAL**                                     | 530   |  67  | 87%   |


