# telegram dependencies
from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
# import my controller script and additional packadfe for logging to console
from kiwi_controller import *
from model.questions import *
import logging

 # log into console - very helpful  stuff
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')



# staff needed for start bot and register in telegram bot system
updater = Updater(TELEGRAM_TOKEN)

#  help to send message periodically,with  set intervals for messsaging
# e.t.c . It runs asynchronously in a separate thread.
job_q = updater.job_queue

# variable question needed for iteraction with a user & give additional
# info how to search throw bot

parameters_for_user_search = []
result_of_search = []

# functions


def get_a_single_question():
    yield from questions


single_question = get_a_single_question()


def iterate_through_questions(bot, update):
    global single_question
    global result_of_search


    try:
        question = next(single_question)

    except:
        single_question = get_a_single_question()
        print("-------------------" + str(parameters_for_user_search))
        # result_of_search = unpack_data(init_search_parameters(parameters_for_user_search[1],parameters_for_user_search[2]))
        result_of_search = init_search_parameters(parameters_for_user_search[1],parameters_for_user_search[2])
        print(result_of_search)
        send_updates_for_users(bot, update)
        parameters_for_user_search.clear()  # empty list for futher use
        result_of_search.clear()
        return
    return question


def search(bot, update):
    parameters_for_user_search.append(update.message.text)
    message_for_user = iterate_through_questions(bot, update)
    try:
        bot.send_message(chat_id=CHAT_ID,
                         text=message_for_user)
    except:
        return




def handle_search(bot, update):
    """Here we set handler to all text masseges and for invoke
    search command """
    handler = MessageHandler(Filters.text | Filters.command, search)
    updater.dispatcher.add_handler(handler)
    # updater.dispatcher.remove_handler(handler)
    search(bot, update)




def send_updates_for_users(bot, job):
    global result_of_search
    couter = 25
    prev_counter = 0
    for it in range(0, int(len(result_of_search) / couter) + 1):
        if len(result_of_search) >= 25:
            bot.send_message(parse_mode='HTML', chat_id=CHAT_ID,
                             text=f'''{''.join(result_of_search[prev_counter:couter])}''')
            prev_counter = couter
            couter *= 2
        else:
            bot.send_message(parse_mode='HTML', chat_id=CHAT_ID,
                             text=result_of_search)







updater.dispatcher.add_handler(CommandHandler('search', handle_search))
# my_updates_sender = job_q.run_repeating(search, interval=90, first=0)

updater.start_polling()
updater.idle()
