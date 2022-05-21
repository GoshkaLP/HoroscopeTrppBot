from os import getenv

# Для отладки
# from dotenv import load_dotenv
# load_dotenv()


class Config:
    """
    Конфиг с настройками приложения Flask
    """
    SECRET_KEY = getenv('FLASK_SECRET')
    DEBUG = False
    TESTING = False
