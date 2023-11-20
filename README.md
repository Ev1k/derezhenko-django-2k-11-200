## Запуск проекта для разработки

- `python3 -m venv env` - создание виртуального окружения
- `source env/Scripts/activate` - войти в виртуальное окружение
- `pip install -r requirements.txt` - установка зависимостей
- `python manage.py migrate` - применение миграций
- `python manage.py runserver` - запустить сервер для разработки на http://127.0.0.1:8000
- `pip install pre-commit && pre-commit install` - установить pre-commit
- `pre-commit run -a` - запустить pre-commit на всём проекте
