from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from kiwi_controller import *
import logging
from threading import Thread

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

questions = [
    'Вкажіть пункт відправлення.Вживайте лише англійські назви міст без спеціальних знаків (наприклад: Krakow).',
    'Тепер вкажіть місто прибуття. Вживайте лише англійські назви міст без спеціальних знаків(наприклад: Kiev).',
    'Хороший вибір! Тепер вкажіть від якої дати шукати  в форматі 10/09/2018',
    ' Тепер вкажіть до якої дати шукати  в форматі 23/11/2018', 'Вкажіть кількість пасажирів. Наприклад 2',
    'Кінець питань']

single_question = ""
user_search = ""







def get_a_single_question():
    """ return single question in  generator type """
    yield from questions

def init():
    """declare generator variable"""
    single_question_generator = get_a_single_question()
    return single_question_generator

def reset_questions():
    """reset single question when StopIteration exception appear"""
    global single_question
    single_question = init()









def search(bot, update, chat_data):
    global handler

    try:
        next_question = next(single_question)
        chat_data[f'{next_question}'] = update.message.text
        print(chat_data)
        bot.send_message(chat_id=update.message.chat_id,
                     text=next_question)
    except:
        reset_questions()
        chat_data.clear()
        updater.dispatcher.remove_handler(handler)



def handle_search(bot, update, chat_data):
        """Here we set handler to all text masseges and for invoke
        search command """
        global handler
        global single_question
        global number

        single_question = init()
        updater.dispatcher.add_handler(handler)
        search(bot, update, chat_data)



#  define a handler for search commmand
handler = MessageHandler(Filters.text | Filters.command, search, pass_chat_data=True)









updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('search', handle_search, pass_chat_data=True))

updater.start_polling()
updater.idle()