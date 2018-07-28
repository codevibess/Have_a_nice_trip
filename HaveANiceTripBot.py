from telegram.ext import Updater, CommandHandler
import logging
from config import *

#  log into console - very helpful  stuff
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(TELEGRAM_TOKEN)
#  help to send message periodically,with  set intervals for messsaging
# e.t.c . It runs asynchronously in a separate thread.
job_q = updater.job_queue



def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))


def send_updates_for_users(bot, job):
    bot.send_message(chat_id=CHAT_ID,
                     text='Update for user')


updater.dispatcher.add_handler(CommandHandler('hello', hello))

my_updates_sender = job_q.run_repeating(send_updates_for_users, interval=90, first=0)

updater.start_polling()
updater.idle()
