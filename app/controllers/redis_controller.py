import redis
from os import getenv
from app.controllers.horoscope_controller import get_zodiacal_sign, get_chinese_sign, parse_zodiacal_forecast, \
    parse_chinese_forecast

# Для отладки
from dotenv import load_dotenv
load_dotenv()


REDIS_HOST = getenv('HOST')
REDIS_PASSWORD = getenv('REDIS_PASSWORD')

redis_con = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    db=0
)


def add_user_zodiacal_sign(user_id, date):
    sign = get_zodiacal_sign(date)
    key = 'user:{}'.format(user_id)
    redis_con.hset(key, 'zodiacal', sign)


def add_user_chinese_sign(user_id, date):
    sign = get_chinese_sign(date)
    key = 'user:{}'.format(user_id)
    redis_con.hset(key, 'chinese', sign)


def get_user_zodiacal_sign(user_id):
    key = 'user:{}'.format(user_id)
    sign = redis_con.hget(key, 'zodiacal')
    if sign:
        return sign


def get_user_chinese_sign(user_id):
    key = 'user:{}'.format(user_id)
    sign = redis_con.hget(key, 'chinese')
    if sign:
        return sign


def update_zodiacal_forecast():
    key = 'forecast:zodiacal'
    for sign, forecast in parse_zodiacal_forecast():
        redis_con.hset(key, sign, forecast)


def update_chinese_forecast():
    key = 'forecast:chinese'
    for sign, forecast in parse_chinese_forecast():
        redis_con.hset(key, sign, forecast)


def get_zodiacal_forecast(sign):
    key = 'forecast:zodiacal'
    forecast = redis_con.hget(key, sign)
    if forecast:
        return forecast.decode()


def get_chinese_forecast(sign):
    key = 'forecast:chinese'
    forecast = redis_con.hget(key, sign)
    if forecast:
        return forecast.decode()
