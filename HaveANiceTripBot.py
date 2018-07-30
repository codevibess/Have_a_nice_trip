from telegram.ext import Updater, CommandHandler

from kiwi_controller import *
import logging
# from config import *

#  log into console - very helpful  stuff
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(TELEGRAM_TOKEN)
#  help to send message periodically,with  set intervals for messsaging
# e.t.c . It runs asynchronously in a separate thread.
job_q = updater.job_queue

x = get_data_by_default_parameters()


def hello(bot, update):
    global x
    bot.send_message(parse_mode='HTML', chat_id=CHAT_ID,
                     text=x)


def send_updates_for_users(bot, job):
    global x
    href ="vk.com"
    while len(x)>10:
        bot.send_message(parse_mode='HTML', chat_id = CHAT_ID,
                     text=x)



updater.dispatcher.add_handler(CommandHandler('hello', send_updates_for_users))

my_updates_sender = job_q.run_repeating(send_updates_for_users, interval=30, first=0)

updater.start_polling()
updater.idle()
