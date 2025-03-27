# README.md

## О проекте

Приложение **Orders** — простая система управления заказами для кафе или
ресторана. Поддерживает создание, редактирование, удаление заказов, фильтрацию,
подсчет выручки и REST API.

## Быстрый старт (Docker Compose)

### Клонирование репозитория

```bash
git clone https://github.com/faiver-90/test_work_eff_mob.git .
```

### Создание файла окружения `.env`

Скопируйте шаблон и заполните переменные:

```bash
cp .env_sample .env
```

Укажите значения для:

- POSTGRES_DB - имя базы данных
- POSTGRES_USER - имя пользователя в базе данных
- POSTGRES_PASSWORD - пароль для пользователя
- POSTGRES_HOST - хост для базы данных, если в докере то db
- POSTGRES_PORT - порт базы данных если отличается от 5432

### Запуск сервисов

```bash
docker-compose up -d --build
```

### Применение миграций

```bash
docker-compose exec web python manage.py migrate
```

### Создание суперпользователя (опционально)

```bash
docker-compose exec web python manage.py createsuperuser
```

### Доступ к приложению

Откройте в браузере:  `http://localhost:9000`

## Использование

### Веб-интерфейс

- Список заказов: `/order/order_list/`
- Создать заказ: `/order/create_order/`
- Редактировать заказ: `/order/<id>/edit/`
- Удалить заказ: `/order/<id>/delete/`
- Выручка: `/order/revenue/`

### REST API

Base URL: `http://localhost:9000/api/`

| Метод    | Endpoint                    | Описание                   |
|----------|-----------------------------|----------------------------|
| GET      | `/orders/`                  | Список заказов             |
| POST     | `/orders/`                  | Создать заказ              |
| GET      | `/orders/<id>/`             | Детали заказа              |
| PUT/PATCH| `/orders/<id>/`             | Обновить заказ             |
| DELETE   | `/orders/<id>/`             | Удалить заказ              |
| GET      | `/revenue/`                 | Общая выручка              |


#### Фильтрация и поиск

Добавьте `?search=<номер_стола или статус>` к запросу списка заказов.

### Примеры работы с API

#### Получение списка заказов

```bash
curl -X GET "http://localhost:9000/api/orders/" -H "Accept: application/json"
```

#### Поиск заказов по номеру стола или статусу

```bash
curl -X GET "http://localhost:9000/api/orders/?search=5" -H "Accept: application/json"
```

#### Создание нового заказа

```bash
curl -X POST "http://localhost:9000/api/orders/" \
  -H "Content-Type: application/json" \
  -d '{"table_number": 5, "item_ids": [1, 2], "status": 1}'
```

#### Получение заказа по ID

```bash
curl -X GET "http://localhost:9000/api/orders/1/" -H "Accept: application/json"
```

#### Полное обновление заказа (PUT)

```bash
curl -X PUT "http://localhost:9000/api/orders/1/" \
  -H "Content-Type: application/json" \
  -d '{"table_number": 5, "item_ids": [1, 3], "status": 2}'
```

#### Частичное обновление заказа (PATCH)

```bash
curl -X PATCH "http://localhost:9000/api/orders/1/" \
  -H "Content-Type: application/json" \
  -d '{"status": 3}'
```

#### Удаление заказа

```bash
curl -X DELETE "http://localhost:9000/api/orders/1/"
```

#### Получение общей выручки

```bash
curl -X GET "http://localhost:9000/api/revenue/" -H "Accept: application/json"
```

## Настройка локального окружения без Docker

1. Создайте виртуальное окружение и активируйте его:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте `.env` и подключитесь к базе данных.
4. Выполните миграции и запустите сервер:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```


