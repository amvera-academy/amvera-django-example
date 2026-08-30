# Django на Amvera

Простой пример деплоя Django в [Amvera](https://amvera.ru). 

Это тестовое приложение показывает работу API, шаблонов, CSRF, статических файлов и персистентное сохранение SQlite в постоянное хранилище Amvera.

[КАК СОХРАНЯТЬ БД](#как-правильно-сохранять-бд) | [СТАТИЧЕСКИЕ ФАЙЛЫ](#статические-файлы) | [CELERY](https://github.com/amvera-academy/amvera-fastapi-example/blob/main/CELERY.md) | [КАК ЗАПУСТИТЬ НА AMVERA](#деплой-в-amvera) 

## Демо-приложение

Приложение имеет веб-интерфейс, на котором вы сразу можете выполнить доступные тестовые запросы. 

- `GET /api/health`
- `GET /api/items`
- `POST /api/items`
- `DELETE /api/items/{id}`

Все запросы можно выполнить на главной странице.

<img width="808" height="888" alt="Screenshot_3" src="https://github.com/user-attachments/assets/c9bb0575-e778-4f82-9cd7-b94869d57577" />

## Как правильно сохранять БД

В разработке очень важно учитывать, что любые изменяемые в процессе работы приложения файлы (базы данных, списки, которые нужно сохранять, JSON и т.п.) **необходимо сохранять в [постоянное хранилище Amvera](https://docs.amvera.ru/applications/storage.html#data)**.

Здесь нет ничего сложного: вместо сохранения БД в той же папке, что код, ее нужно сохранять по пути `/data` (это значение по умолчанию, его можно сменить во вкладке "Конфигурация" вашего проекта).

Например:
```python
DATA_DIR = Path("/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_DIR / "items.sqlite3",
    }
}
```

## Статические файлы

Файлы находятся в директории static. Команда `collectstatic` собирает их в staticfiles, после чего WhiteNoise раздает их через Django-приложение.

Пример:

```django
{% load static %}
<link rel="stylesheet" href="{% static 'styles.css' %}">
```

## Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:5000
```

Откройте localhost:5000.

## Деплой в Amvera

Для деплоя конкретно этого приложения вам понадобится:
1. Создать аккаунт в [Amvera](https://cloud.amvera.ru);
2. Создать обычное приложение в любом регионе;
3. Загрузить в него код репозитория;
4. Во вкладке "Конфигурация" нажать кнопку "Собрать".

Когда приложение будет готово к работе и статус сменится на "Запущено", во вкладке "Домены" можно будет создать бесплатное доменное имя от Амвера.

Добавьте переменную `SECRET_KEY`. 


Отдельный пример фоновой задачи и worker описан в общей [инструкции по Celery](https://github.com/amvera-academy/amvera-fastapi-example/blob/main/CELERY.md).
