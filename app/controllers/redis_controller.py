import redis
from os import getenv, name
from app.controllers.horoscope_controller import get_zodiacal_sign, get_chinese_sign, parse_zodiacal_forecast, \
    parse_chinese_forecast

from datetime import datetime

# Для отладки
# from dotenv import load_dotenv
# load_dotenv()

# Необходимые переменные
REDIS_HOST = getenv('REDIS_HOST')
if name == 'posix':
    REDIS_HOST = 'trpp_redis'
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

# Создание подключения к Redis
redis_con = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    db=0,
    password=REDIS_PASSWORD
)


def get_last_update_time():
    """
    Функция для получения из Redis последнего времени обновления гороскопов
    :return: None | datetime.datetime
    """
    key = 'forecast'
    data = redis_con.hget(key, 'update_time')
    if data:
        date = datetime.strptime(data.decode(), '%d.%m.%Y %H:%M')
        return date
    return None


def set_last_update_time():
    """
    Функция для установки последнего времени обновления гороскопов
    :return:
    """
    key = 'forecast'
    current_datetime = datetime.utcnow()
    data = current_datetime.strftime('%d.%m.%Y %H:%M')
    redis_con.hset(key, 'update_time', data)


def add_user_zodiacal_sign(user_id, date):
    """
    Функция для сохранения знака зодиака пользтвателя
    :param user_id: id пользователя в Telegram
    :param date: дата рождения пользователя
    :return:
    """
    sign = get_zodiacal_sign(date)
    key = 'user:{}'.format(user_id)
    redis_con.hset(key, 'zodiacal', sign)


def add_user_chinese_sign(user_id, date):
    """
    Функция для сохранения китайского знака пользователя
    :param user_id: id пользователя в Telegram
    :param date: дата рождения пользователя
    :return:
    """
    sign = get_chinese_sign(date)
    key = 'user:{}'.format(user_id)
    redis_con.hset(key, 'chinese', sign)


def get_user_zodiacal_sign(user_id):
    """
    Функция для получения знака зодиака пользователя
    :param user_id: id пользователя в Telegram
    :return: None | str
    """
    key = 'user:{}'.format(user_id)
    sign = redis_con.hget(key, 'zodiacal')
    if sign:
        return sign.decode()


def get_user_chinese_sign(user_id):
    """
    Функция для получения китайского знака пользователя
    :param user_id: id пользователя в Telegram
    :return: None | str
    """
    key = 'user:{}'.format(user_id)
    sign = redis_con.hget(key, 'chinese')
    if sign:
        return sign.decode()


def update_zodiacal_forecast():
    """
    Функция для обновления знаков зодиака
    :return:
    """
    key = 'forecast:zodiacal'
    for sign, forecast in parse_zodiacal_forecast():
        redis_con.hset(key, sign, forecast)


def update_chinese_forecast():
    """
    Функция для обновления китайских знаков
    :return:
    """
    key = 'forecast:chinese'
    for sign, forecast in parse_chinese_forecast():
        redis_con.hset(key, sign, forecast)


def update_forecasts():
    """
    Метод для обновления всех гороскопов, если прошел 1 день или более с последнего обновления
    :return:
    """
    current_time = datetime.utcnow()
    last_update_time = get_last_update_time()
    if not last_update_time or (current_time - last_update_time).days >= 1:
        update_zodiacal_forecast()
        update_chinese_forecast()
        set_last_update_time()


def get_zodiacal_forecast(sign):
    """
    Получить прогноз для знака зодиака
    :param sign: знак зодиака
    :return: None | str
    """
    key = 'forecast:zodiacal'
    forecast = redis_con.hget(key, sign)
    if forecast:
        return forecast.decode()


def get_chinese_forecast(sign):
    """
    Получить прогноз для китайского знака
    :param sign: знак
    :return: None | str
    """
    key = 'forecast:chinese'
    forecast = redis_con.hget(key, sign)
    if forecast:
        return forecast.decode()
