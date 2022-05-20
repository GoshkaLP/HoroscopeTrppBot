import telebot
from os import getenv

# Для отладки
from dotenv import load_dotenv
load_dotenv()

TOKEN = getenv('TG_TOKEN')
BASE_URl = getenv('BASE_URL')


bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()


zodiacal = {
    'aries': 'Овен',
    'taurus': 'Телец',
    'gemini': 'Близнецы',
    'cancer': 'Рак',
    'lion': 'Лев',
    'virgo': 'Дева',
    'libra': 'Весы',
    'scorpio': 'Скорпион',
    'sagittarius': 'Стрелец',
    'capricorn': 'Козерог',
    'aquarius': 'Водолей',
    'pisces': 'Рыбы'
}

chinese = {
    'rat': 'Крыса',
    'ox': 'Вол',
    'tiger': 'Тигр',
    'hare': 'Заяц',
    'dragon': 'Дракон',
    'snake': 'Змея',
    'horse': 'Лощадь',
    'goat': 'Коза',
    'monk': 'Обезьяна',
    'cock': 'Петух',
    'dog': 'Собака',
    'pig': 'Свинья'
}


@bot.message_handler(func=lambda message: True)
def test(message):
    bot.reply_to(message, "asdsad")


bot.infinity_polling()
