## Оглавление
+ [Описание проекта](#описание-проекта)
+ [Быстрый старт](#быстрый-старт)
    + [Предварительные требования для запуска](#предварительные-требования-для-запуска)
    + [Установка и запуск](#установка-и-запуск)
    + [Метрики и визуализация](#метрики-и-визуализация)
    + [API документация](#api-документация)
+ [Описание инфраструктуры](#описание-инфраструктуры)
    + [Структура проекта](#структура-проекта)
    + [Описание компонентов проекта](#описание-компонентов-проекта)
+ [Сборка приложения](#сборка-приложения)
    + [Предварительные требования для сборки](#предварительные-требования-для-сборки)
    + [Установка Poetry](#установка-poetry)
    + [Установка и настройка проекта](#установка-и-настройка-проекта)
    + [Установка зависимостей и активация виртуального окружения](#установка-зависимостей-и-активация-виртуального-окружения)
+ [Тестирование приложения](#тестирование-приложения)
    + [Линтинг с pre-commit](#линтинг-с-pre-commit)
    + [Тестирование с pytest](#тестирование-с-pytest)
      
## Описание проекта
Асинхронное  backend-приложения на FastAPI, реализующеий API социальной сети с готовым frontend интерфейсом.  

**Технологический стек:**
- FastAPI – основной фреймворк;
- Uvicorn - ASGI-сервер для запуска FastAPI приложения;
- SQLAlchemy – ORM;
- PostgreSQL - СУБД;
- Alembic - миграции;
- Prometheus - система мониторинга и сбора метрик;
- Grafana - платформа для визуализации метрик;
- Pydantic – валидация входных/выходных данных;
- bcrypt – хэширование чувствительных данных пользователей с генерацией “соли”;
- Nginx – отдача статики и проксирования HTTP-запросов на backend;
- Docker compose – контейнеризация сервисов;
- Pytest – покрытие проекта тестами в соответствии с пирамидой тестирования (unit/integration/e2e);
- Pre-commit config – проверка кода линтерами с хуками;
- Logging – централизованное логирование через mddleware.  

**Функционал приложения** 

Пользователь переходит на сайт с уже имеющимся у себя ключом (`api_key`) для авторизации.
На стороне фронтенда разработана небольшая форма, в которую можно
подставить ключ для пользователя на бэкенде (по умполчанию `api_key=test`). 

При запуске проекта в базе данных уже будут находиться два пользователя с ключами `test` и `dev` - используя эти ключи, 
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


## Быстрый старт

### Предварительные требования для запуска
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

   GRAFANA_USER=admin
   GRAFANA_PASS=admin
3. Разверните проект через Docker Compose
   
   ```
   docker compose up --build
4. Перейдите в браузер по ссылке
   
   ```
   http://localhost:8080/
   ```

### Метрики и визуализация
- Grafana (для авторизации ввести логин и пароль из .env-файла)
  ```
  http://localhost:3000/
  ```
- Prometheus
  ```
  http://localhost:8000/metrics
  ```

### API документация
- Swagger UI
  ```
  http://localhost:8000/docs
  ```
- ReDoc
  ```
  http://localhost:8000/redoc
  ```
## Описание инфраструктуры
### Структура проекта

Приложение построено по принципам REST и архитектурному шаблону MVC. Все модули разделены на независимые компоненты, обеспечивая читаемость, масштабируемость и тестируемость кода.

```
twitter-clone/  
├── alembic/                      # Миграции базы данных  
├── client/                       # Client - фронтенд и nginx
│   ├── static/                   # Фронтенд  
│   ├── Dockerfile                # Конфигурация Docker для статики  
│   └── nginx.conf                # Конфигурация Nginx
├── grafana/                      # Конфигурация для Grafana 
│   └── provisioning/             # Автоматическая настройка Grafana
│       ├── dashboards/           # конфигурация dashboards
│       └── datasources/          # Конфигурация источников данных (Prometheus)
├── prometheus/                   # Конфигурация для Prometheus
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

### Описание компонентов проекта

**Функциональность проекта**
- Авторизация и аутентификация пользователей через api_key;
- Работа с постами: создание, удаление, лайк, загрузка медиа-файлов;
- Подписка на пользователей;
- Лента постов с сортировкой по популярности в порядке убывания (по количеству лайков) и поддержкой пагинации.

**Авторизация пользователя**  
Пользователь переходит на сайт с уже имеющимся у себя ключом (api_key) для авторизации. На стороне фронтенда разработана форма, в которую необходимо подставить ключ. Для безопасного хранения ключей реализовано хэширование с “солью” через bcrypt. 
 
**Аутентификация пользователя**  
Все эндпоинты имеют http-header с названием api_key.  Проверка ключа реализована через Depends-зависимость FastAPI, где при запросах из http-header извлекается значение api_key и находится нужный пользователь в базе данных, тем самым подтверждая его личность.
	
**Взаимодействие с ресурсами**  
Все клиентские запросы проходят через nginx с проксированием на backend. На стороне бэкенда данные проходят валидацию через Pydantic, затем выполняются необходимые crud-операции с базой данных. После этого ответ снова проходит валидацию и отправляется клиенту через Nginx. Статические файлы (frontend и медиа) отдаются напрямую через Nginx. Ответы API формируются с помощью ORJSONResponse для ускорения обработки.
	
 **Обработка ошибок и логирование**  
Реализована централизованная система обработки исключений через FastAPI обработчики с возвратом стандартного JSON ответа (код, тип и описание ошибки). Ведение логов осуществляется через logging с промежуточным middleware слоем.
	
 **Проверка кода**  
В проекте используются Git-хуки с pre-commit для запуска проверки кода линтерами (black, isort, flake8, mypy), а также тестирование приложения с pytest, которое включает в себя unit-тестирование, integration, system (e2e).
	
 **Gitlab (не актуально для Github; как пример)**  
GitLab CI настроен на запуск пайплайна при merge_request_event. Репозиторий с проектом настроен на запрет слияния, если хотя бы одна стадия CI не прошла. Пайплайн включает стадии сборки, линтинга и тестирования.
	
 **Безопасность и защита данных**  
Api-key пользователей хранятся в виде bcrypt-хешей с уникальной “солью”, что исключает возможность восстановления исходных данных. Все SQL-запросы выполняются через параметризированные методы SQLAlchemy, без конкатенации строк, что полностью исключает риск SQL-инъекций. 

**Мониторинг и аналитика**  
Система мониторинга реализована на базе Prometheus для сбора метрик с FastAPI-приложения через эндпоинт /metrics и Grafana с предустановленными в проекте JSON-дашбордами для визуализации этих данных и настроенным Prometheus.

**Инфраструктура и контейнеризация**  
Каждый компонент проекта (PostgreSQL, Nginx, FastAPI, Prometheus, Grafana) размещён в отдельном Docker контейнере с общей сетью. Задана последовательность запуска и проверки работоспособности сервисов через директивы depends_on и healthcheck.


## Сборка приложения
### Предварительные требования для сборки
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

   GRAFANA_USER=admin
   GRAFANA_PASS=admin
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

## Тестирование приложения
Перед тестированием приложения должны быть выполнены все пункты из раздела **Сборка приложения (dev)**
### Линтинг с pre-commit
- Для проверки кода линтерами используйте команду:

  ```bash
  pre-commit run --all-files
  ```

### Тестирование с pytest
- Для тестирования приожения используйте команду:
  
  ```bash
  pytest -v ./tests
  ```
- Для вывод отчёта о покрытии приложения тестами введите:
  
   ```bash
   pytest --cov=./server
   ```
**Таблица с отчётом о покрытии тестами**  
**Общее покрытие:** 87% (524 строк кода, 67 пропущено)

| Файл                                          | Строк | Пропущено | Покрытие |
|-----------------------------------------------|:-----:|:----:|:-----:|
| `server/api/crud/crud_likes.py`               |  17   |  0   | 100%  |
| `server/api/crud/crud_medias.py`              |  16   |  0   | 100%  |
| `server/api/crud/crud_tweets.py`              |  44   |  5   | 89%   |
| `server/api/crud/crud_users.py`               |  30   |  0   | 100%  |
| `server/api/routes/__init__.py`               |   8   |  0   | 100%  |
| `server/api/routes/routes_medias.py`          |  13   |  1   | 92%   |
| `server/api/routes/routes_tweets.py`          |  31   |  5   | 84%   |
| `server/api/routes/routes_users.py`           |  25   |  4   | 84%   |
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
| `server/core/schemas/schemas_base.py`         |  24   |  0   | 100%  |
| `server/core/schemas/schemas_likes.py`        |   9   |  1   | 89%   |
| `server/core/schemas/schemas_medias.py`       |   4   |  0   | 100%  |
| `server/core/schemas/schemas_tweets.py`       |  23   |  0   | 100%  |
| `server/core/schemas/schemas_users.py`        |  10   |  0   | 100%  |
| `server/create_app.py`                        |  23   |  3   | 87%   |
| `server/error_handlers.py`                    |  18   |  2   | 89%   |
| `server/main.py`                              |   6   |  1   | 83%   |
| `server/utils/create_mock_data.py`            |  26   |  21  | 19%   |
| `server/utils/hashed_api_key.py`              |   7   |  0   | 100%  |
| `server/utils/media_writer.py`                |  38   |  6   | 84%   |
| **TOTAL**                                     | 524   |  67  | 87%   |
