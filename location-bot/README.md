# 📦 service_2

**service_2** — это Telegram-бот на Python, использующий Supabase в качестве облачной базы данных. Предназначен для управления и взаимодействия с пользователями через Telegram, с хранением данных в Supabase.

---

## 🔧 Технологии

- Python 3.8+
- [aiogram](https://github.com/aiogram/aiogram) — Telegram Bot Framework
- [Supabase](https://supabase.com) — Backend-as-a-Service
- Docker (опционально)

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/Ponomarev49/service_2.git
cd service_2
```

### 2. Создайте файл `.env`

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
SUPABASE_KEY=<YOUR_SUPABASE_API_KEY>
SUPABASE_URL=<YOUR_SUPABASE_PROJECT_URL>
```

> ⚠️ **Никогда не публикуйте реальные токены и ключи API в открытом доступе.**

### 3. Установите зависимости

```bash
pip install -r requirements.txt
```

### 4. Запустите бота

```bash
python bot.py
```

---

## 🐳 Запуск с Docker

```bash
docker build -t service_2 .
docker run --env-file .env service_2
```

---

## 🗂 Структура проекта

```
.
├── bot.py                 # Точка входа
├── core/                  # Основная логика
├── database/              # Работа с Supabase
├── utils/                 # Вспомогательные функции
├── requirements.txt       # Зависимости
├── Dockerfile             # Docker-сборка
└── .env                   # Переменные окружения (не добавляйте в Git)
```
