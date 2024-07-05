# Telegram_parser

## Функционал
- Парсинг с выводом в Google_sheets и excel;
- Интервальный парсинг;
- Отслеживание продуктов по их свойствам;
- Уведомление о появлении новых товаров;

## Установка
python==3.9.7
```sh
python -m venv venv
venv\Scripts\activate
pip install -r .\requirements.txt
python manage.py app.py
```

## Получение токена
Токен можно получить у @BotFather, затем нужно вставить его в config.py

## ВАЖНО!
- Бот больше не работает, т.к WildBerries поменяли структуру данных и парсер необходимо доработать, либо вовсе заменить
