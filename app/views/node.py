from flask import Blueprint, request
from telebot import types

from app.controllers.bot_controller import bot, TG_SECRET

node = Blueprint('node', __name__)


@node.route('/{}'.format(TG_SECRET), methods=['POST'])
def tg_handler():
    """
    Route для обработки новых обновлений от Telegram
    :return:
    """
    bot.process_new_updates([types.Update.de_json(request.get_data().decode('utf-8'))])
    return 'ok', 200
