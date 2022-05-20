from os import getenv
# Для отладки
from dotenv import load_dotenv
load_dotenv()


class Config:
    SECRET_KEY = getenv('FLASK_SECRET')
    DEBUG = False
    TESTING = False
