from app import create_app
from config import Config

app = create_app(Config)

if __name__ == '__main__':
    """
    Запуск приложения на Flask
    """
    app.run(host='0.0.0.0', port=8025)
