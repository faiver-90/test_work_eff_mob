# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем проект
COPY . .

# Команда по умолчанию (можно изменить в docker-compose)
CMD ["gunicorn", "project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
