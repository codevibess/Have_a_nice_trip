from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler


from kiwi_controller import *

import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

questions = [
    'Вкажіть пункт відправлення.Вживайте лише англійські назви міст без спеціальних знаків (наприклад: Krakow).',
    'Тепер вкажіть місто прибуття. Вживайте лише англійські назви міст без спеціальних знаків(наприклад: Kiev).',
    'Хороший вибір! Тепер вкажіть від якої дати шукати  в форматі 10/09/2018',
    ' Тепер вкажіть до якої дати шукати  в форматі 23/11/2018', 'Вкажіть кількість пасажирів. Наприклад 2']



def get_a_single_question():
    """ return single question in  generator type """
    yield from questions

def init():
    """declare generator variable"""
    single_question_generator = get_a_single_question()
    return single_question_generator

single_question = init()

def reset_questions():
    """reset single question when StopIteration exception appear"""
    global single_question
    single_question = init()



def search(bot, update):
    try:
        bot.send_message(chat_id=update.message.chat_id,
                     text=next(single_question))
    except:
        reset_questions()
















updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('search', search))

updater.start_polling()
updater.idle()