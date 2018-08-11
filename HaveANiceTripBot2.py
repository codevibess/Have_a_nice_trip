from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from kiwi_controller import *
from model.questions import *
import logging
from threading import Thread

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)



single_question = ""
user_search = ""



def get_a_single_question():
    """ return single question in  generator type """
    yield from questions

def init():
    """declare generator variable"""
    single_question_generator = get_a_single_question()
    return single_question_generator

def reset_questions_and_remove_search_handler():
    """reset single question when StopIteration exception appear"""
    global single_question
    single_question = init()
    updater.dispatcher.remove_handler(handler)









def search(bot, update, chat_data):
    global handler

    try:
        next_question = next(single_question)

        chat_data[f'{next_question}'] = update.message.text
        print(chat_data)
        print(chat_data[f'{CITY_FROM}'])
        bot.send_message(chat_id=update.message.chat_id,
                     text=next_question)
    except:
        result_of_user_search = init_search_parameters(chat_data[f'{CITY_TO}'],
                                                       chat_data[f'{DATA_FROM}'],
                                                       # chat_data[f'{DATA_FROM}'],
                                                       # chat_data[f'{DATA_TO}']

        )
        print(result_of_user_search)
        try:
            send_updates_for_users(result_of_user_search,bot, update)
        except:
            print("BAD REQUEST")
        finally:
            reset_questions_and_remove_search_handler()
            reset()
            print(fly_from)
            chat_data.clear()




def handle_search(bot, update, chat_data):
        """Here we set handler to all text masseges and for invoke
        search command """
        global handler
        global single_question

        single_question = init()
        updater.dispatcher.add_handler(handler)
        search(bot, update, chat_data)


def check(bot, update):
    low_cost_result = get_data_by_default_parameters()

    send_updates_for_users(low_cost_result,bot, update)

def send_updates_for_users(result_of_search, bot, update):
        couter = 25
        prev_counter = 0

        for it in range(0, int(len(result_of_search) / couter) + 1):
            if len(result_of_search) >= 25:
                bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,
                                 text=f'''{''.join(result_of_search[prev_counter:couter])}''')
                prev_counter = couter
                couter *= 2
            else:
                bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,
                                 text=f'''{''.join(result_of_search[1:10])}''')



#  define a handler for search commmand
handler = MessageHandler(Filters.text | Filters.command, search, pass_chat_data=True)









updater = Updater(TELEGRAM_TOKEN)

updater.dispatcher.add_handler(CommandHandler('search', handle_search, pass_chat_data=True))
updater.dispatcher.add_handler(CommandHandler('check', check))

updater.start_polling()
updater.idle()