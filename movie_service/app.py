# movie_service/app.py

from flask import Flask
from movie_service.routes import movies_bp # Імпортуємо наш Blueprint
import os

# Створюємо функцію-фабрику додатків
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Налаштування конфігурації
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Тут можуть бути інші налаштування, наприклад, для бази даних
    )

    if test_config is None:
        # Завантажити конфігурацію, якщо вона існує, під час не-тестового запуску
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Завантажити тестову конфігурацію
        app.config.from_mapping(test_config)

    # Переконатися, що папка instance існує
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(movies_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    print("Movie Service ?????? ?? ????? 5001...")
    app.run(debug=True, port=5001)