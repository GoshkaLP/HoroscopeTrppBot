import requests as r
from bs4 import BeautifulSoup
from datetime import datetime


# Знаки зодиака
zodiacal_signs = ['aries', 'taurus', 'gemini', 'cancer', 'lion', 'virgo',
                  'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']

# Китайские знаки
chinese_signs = ['rat', 'ox', 'tiger', 'hare', 'dragon', 'snake', 'horse', 'goat', 'monk', 'cock', 'dog', 'pig']

# Header для запросов
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/70.0.3538.77 Safari/537.36'
}

# URL с прогнозами
zodiac_url = 'https://orakul.com/horo-ajax/many-date-view/astrologic/more/today/{}'
chinese_url = 'https://orakul.com/horo-ajax/many-date-view/chinese/general/today/{}'


def get_forecast(url):
    """
    Основная функция, который парсит сайт с горосками и вытаскивает прогнозы
    :param url: ссылка на прогнозы
    :return: str
    """
    req = r.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'lxml')
    forecast = soup.find('div', class_='\\"horoBlock\\"').find('p', attrs={'class': True}).text.encode(). \
        decode('unicode-escape').strip()
    forecast = forecast[:forecast.rfind('.')+1]
    return forecast


def get_zodiacal_sign(birth_date):
    """
    Функция для получения знака зодиака по дате рождения
    :param birth_date: дата рождения
    :return: str
    """
    year = birth_date.year
    if datetime(day=21, month=3, year=year) <= birth_date <= datetime(day=19, month=4, year=year):
        return 'aries'
    elif datetime(day=20, month=4, year=year) <= birth_date <= datetime(day=20, month=5, year=year):
        return 'taurus'
    elif datetime(day=21, month=5, year=year) <= birth_date <= datetime(day=20, month=6, year=year):
        return 'gemini'
    elif datetime(day=21, month=6, year=year) <= birth_date <= datetime(day=22, month=7, year=year):
        return 'cancer'
    elif datetime(day=23, month=7, year=year) <= birth_date <= datetime(day=22, month=8, year=year):
        return 'lion'
    elif datetime(day=23, month=8, year=year) <= birth_date <= datetime(day=22, month=9, year=year):
        return 'virgo'
    elif datetime(day=23, month=9, year=year) <= birth_date <= datetime(day=22, month=10, year=year):
        return 'libra'
    elif datetime(day=23, month=10, year=year) <= birth_date <= datetime(day=21, month=11, year=year):
        return 'scorpio'
    elif datetime(day=22, month=11, year=year) <= birth_date <= datetime(day=21, month=12, year=year):
        return 'sagittarius'
    elif datetime(day=22, month=12, year=year) <= birth_date <= datetime(day=19, month=1, year=year):
        return 'capricorn'
    elif datetime(day=20, month=1, year=year) <= birth_date <= datetime(day=18, month=2, year=year):
        return 'aquarius'
    elif datetime(day=19, month=2, year=year) <= birth_date <= datetime(day=20, month=3, year=year):
        return 'pisces'


def get_chinese_sign(birth_date):
    """
    Функция для получения китайского знака по году рождения
    :param birth_date: дата рождения
    :return: str
    """
    year = birth_date.year
    if (year - 1900) % 12 == 0:
        return 'rat'
    elif (year - 1901) % 12 == 0:
        return 'ox'
    elif (year - 1902) % 12 == 0:
        return 'tiger'
    elif (year - 1903) % 12 == 0:
        return 'hare'
    elif (year - 1904) % 12 == 0:
        return 'dragon'
    elif (year - 1905) % 12 == 0:
        return 'snake'
    elif (year - 1906) % 12 == 0:
        return 'horse'
    elif (year - 1907) % 12 == 0:
        return 'goat'
    elif (year - 1908) % 12 == 0:
        return 'monk'
    elif (year - 1909) % 12 == 0:
        return 'cock'
    elif (year - 1910) % 12 == 0:
        return 'dog'
    elif (year - 1911) % 12 == 0:
        return 'pig'


def parse_zodiacal_forecast():
    """
    Выгрузка прогнозов для знаков зодиака
    :return: tuple
    """
    for sign in zodiacal_signs:
        yield sign, get_forecast(zodiac_url.format(sign))


def parse_chinese_forecast():
    """
    Выгрузка прогнозов для китайских знаков
    :return: tuple
    """
    for sign in chinese_signs:
        yield sign, get_forecast(chinese_url.format(sign))
