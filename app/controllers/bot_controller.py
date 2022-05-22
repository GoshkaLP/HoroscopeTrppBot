import telebot
from telebot import types
from os import getenv

from app.controllers.redis_controller import get_zodiacal_forecast, get_chinese_forecast, update_forecasts, \
    get_user_chinese_sign, get_user_zodiacal_sign, add_user_chinese_sign, add_user_zodiacal_sign

from datetime import datetime

# Для отладки
# from dotenv import load_dotenv
# load_dotenv()

# Необходимые переменные
TOKEN = getenv('TG_TOKEN')
BASE_URl = getenv('BASE_URL')
TG_SECRET = getenv('TG_SECRET')


bot = telebot.TeleBot(TOKEN)
bot.remove_webhook()


# Словарь со знаками зодиака
zodiacal = {
    'Овен ♈': 'aries',
    'Телец ♉': 'taurus',
    'Близнецы ♊': 'gemini',
    'Рак ♋': 'cancer',
    'Лев ♌': 'lion',
    'Дева ♍': 'virgo',
    'Весы ♎': 'libra',
    'Скорпион ♏': 'scorpio',
    'Стрелец ♐': 'sagittarius',
    'Козерог ♑': 'capricorn',
    'Водолей ♒': 'aquarius',
    'Рыбы ♓': 'pisces'
}

# Словарь с китайскими знаками
chinese = {
    'Крыса 🐀': 'rat',
    'Вол 🐂': 'ox',
    'Тигр 🐅': 'tiger',
    'Заяц 🐇': 'hare',
    'Дракон 🐉': 'dragon',
    'Змея 🐍': 'snake',
    'Лошадь 🐎': 'horse',
    'Коза 🐐': 'goat',
    'Обезьяна 🐒': 'monk',
    'Петух 🐓': 'cock',
    'Собака 🐕': 'dog',
    'Свинья 🐖': 'pig'
}


@bot.message_handler(commands=['start', 'help'])
def start_handler(message):
    """
    Функция, обрабатывающая команды бота /start и /help
    Выводит справку о боте
    :param message: входящее сообщение
    :return:
    """
    mes = 'Привет! Данный бот поможет узнать зодиакальный и китайский гороскоп на каждый день! ' \
          'Отправьте команду `/forecast`, чтобы начать!'
    bot.reply_to(message, mes, parse_mode='Markdown')


@bot.message_handler(commands=['set_sign'])
def save_user_sign_start(message):
    """
    Функция, обрабатывающая команду бота /set_sign
    Позволяет сохранить знаки по дате рождения пользователя
    :param message: входящее сообщение
    :return:
    """
    bot.reply_to(message, 'Введите вашу дату рождения в формате: DD.MM.YYYY')
    bot.register_next_step_handler(message, save_user_sign_finish)


def save_user_sign_finish(message):
    """
    Функция, заверщающая процесс сохранения знаков пользователя
    :param message: входящее сообщение
    :return:
    """
    try:
        user_id = message.from_user.id
        try:
            birth_date = datetime.strptime(message.text, '%d.%m.%Y')
            add_user_chinese_sign(user_id, birth_date)
            add_user_zodiacal_sign(user_id, birth_date)
            bot.reply_to(message, 'Ваши *китайский знак* и *знак зодиака* были сохранены!',
                         parse_mode='Markdown')
        except:
            bot.reply_to(message, 'Вы ввели дату в неверном формате! 😵‍💫')
    except:
        bot.reply_to(message, 'Произошла ошибка! Попробуйте еще раз!')


@bot.message_handler(commands=['get_sign'])
def get_user_sign(message):
    """
    Функция, обрабатывающая команду бота /get_sign
    Позволяет получить знаки пользователя, если он их ранее сохранял
    :param message: входящее сообщение
    :return:
    """
    user_id = message.from_user.id
    zodiacal_sign = get_user_zodiacal_sign(user_id)
    chinese_sign = get_user_chinese_sign(user_id)
    if zodiacal_sign and chinese_sign:
        zodiacal_sign_text = list(zodiacal.keys())[list(zodiacal.values()).index(zodiacal_sign)]
        chinese_sign_text = list(chinese.keys())[list(chinese.values()).index(chinese_sign)]
        bot.reply_to(message, 'Ваш *знак зодиака*: {}\n'
                              'Ваш *китайский знак*: {}'.format(zodiacal_sign_text, chinese_sign_text),
                     parse_mode='Markdown')
    else:
        bot.reply_to(message, 'Вы не сохраняли вашу дату рождения! 🤭')


@bot.message_handler(commands=['forecast'])
def forecast_start(message):
    """
    Функция, начинающая обработку команды /forecast
    Данная команда позволяет получить прогноз на сегодня
    :param message: входящее сообщение
    :return:
    """
    markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True, selective=True)
    markup.add(types.KeyboardButton('Зодиакальный гороскоп 🔮'))
    markup.add(types.KeyboardButton('Китайский гороскоп 🥡'))
    bot.reply_to(message, 'Выберите интересующий гороскоп:', reply_markup=markup)
    bot.register_next_step_handler(message, forecast_choice)


@bot.message_handler(func=lambda m: m.text in ['Зодиакальный гороскоп 🔮', 'Китайский гороскоп 🥡'])
def forecast_choice(message):
    """
    Функция, продолжающая обработку команды /forecast
    В зависимости от выбранного типа прогноза показывает доступные знаки
    :param message: входящее сообщение
    :return:
    """
    try:
        user_id = message.from_user.id
        if message.text == 'Зодиакальный гороскоп 🔮':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
            user_zodiacal_sign = get_user_zodiacal_sign(user_id)
            if user_zodiacal_sign:
                user_zodiacal_sign_text = 'Ваш зодиакальный знак: {}'.format(
                    list(zodiacal.keys())[list(zodiacal.values()).index(user_zodiacal_sign)]
                )
                markup.row(user_zodiacal_sign_text)
            for sign in zodiacal.keys():
                markup.row(sign)
            bot.reply_to(message, 'Выберите знак зодиака', reply_markup=markup)
            bot.register_next_step_handler(message, forecast_zodiacal)
        elif message.text == 'Китайский гороскоп 🥡':
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
            user_chinese_sign = get_user_chinese_sign(user_id)
            if user_chinese_sign:
                user_chinese_sign_text = 'Ваш китайский знак: {}'.format(
                    list(chinese.keys())[list(chinese.values()).index(user_chinese_sign)]
                )
                markup.row(user_chinese_sign_text)
            for sign in chinese.keys():
                markup.row(sign)
            bot.reply_to(message, 'Выберите китайский знак', reply_markup=markup)
            bot.register_next_step_handler(message, forecast_chinese)
        else:
            bot.reply_to(message, 'Вы выбрали неверный гороскоп, попробуйте еще раз!')
    except:
        bot.reply_to(message, 'Произошла ошибка! Попробуйте еще раз!')


@bot.message_handler(func=lambda m: m.text in list(zodiacal.keys()) or m.text.find('Ваш зодиакальный знак:') == 0)
def forecast_zodiacal(message):
    """
    Функция, продолжающая обработку команды /forecast
    Выводит пользователю прогноз по выбранному знаку зодиака
    :param message: входящее сообщение
    :return:
    """
    try:
        sign_text = message.text
        if 'Ваш' in sign_text:
            sign_text = sign_text.split(': ')[-1]
        sign = zodiacal.get(sign_text)
        if not sign:
            bot.reply_to(message, 'Неверный знак зодиака! 🤯')
            return
        forecast = get_zodiacal_forecast(sign)
        if not forecast:
            bot.reply_to(message, 'К сожалению, гороскоп для данного знака зодиака не был найден 😟')
            return
        bot.reply_to(message, '*Гороскоп на сегодня:*\n{}'.format(forecast), parse_mode='Markdown')
    except:
        bot.reply_to(message, 'Произошла ошибка! Попробуйте еще раз!')


@bot.message_handler(func=lambda m: m.text in list(chinese.keys()) or m.text.find('Ваш китайский знак:') == 0)
def forecast_chinese(message):
    """
    Функция, продолжающая обработку команды /forecast
    Выводит пользователю прогноз по выбранному китайскому знаку
    :param message: входящее сообщение
    :return:
    """
    try:
        sign_text = message.text
        if 'Ваш' in sign_text:
            sign_text = sign_text.split(': ')[-1]
        sign = chinese.get(sign_text)
        if not sign:
            bot.reply_to(message, 'Неверный знак! 🤕')
            return
        forecast = get_chinese_forecast(sign)
        if not forecast:
            bot.reply_to(message, 'К сожалению, гороскоп для данного знака не был найден 😟')
            return
        bot.reply_to(message, '*Гороскоп на сегодня:*\n{}'.format(forecast), parse_mode='Markdown')
    except:
        bot.reply_to(message, 'Произошла ошибка! Попробуйте еще раз!')


# update_forecasts()
# bot.infinity_polling()


bot.set_webhook('{}/{}'.format(BASE_URl, TG_SECRET))
