# Используем Python 3.11 в качестве базового образа
FROM python:3.12.6-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости через Poetry
RUN poetry install --no-interaction --no-ansi --no-root

# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "fastapi_app.py"]

