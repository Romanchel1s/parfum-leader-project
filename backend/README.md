# Back Bot 2 Parfum

## Описание проекта
Back Bot 2 Parfum - это бэкенд-сервис, разработанный с использованием FastAPI для управления данными парфюмерной продукции.

## Технологии
- Python 3.12
- FastAPI
- Poetry (для управления зависимостями)
- Supabase (для работы с базой данных)
- Docker

## Требования
- Python 3.12 или выше
- Poetry
- Docker (опционально, для запуска в контейнере)

## Установка и запуск

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/back_bot_2_parfum.git
cd back_bot_2_parfum
```

2. Установите зависимости с помощью Poetry:
```bash
poetry install
```

3. Запустите приложение:
```bash
poetry run python fastapi_app.py
```

### Запуск в Docker

1. Соберите Docker-образ:
```bash
docker build -t back-bot-2-parfum .
```

2. Запустите контейнер:
```bash
docker run -p 8000:8000 back-bot-2-parfum
```

## Структура проекта
```
back_bot_2_parfum/
├── fastapi_app.py      # Основной файл приложения
├── config.py          # Конфигурация приложения
├── src/               # Исходный код
├── Dockerfile         # Конфигурация Docker
├── pyproject.toml     # Зависимости проекта
└── poetry.lock        # Фиксированные версии зависимостей
```

## API Endpoints
API будет доступно по адресу: http://localhost:8000

## Логирование
Логи приложения сохраняются в файл `app.log`