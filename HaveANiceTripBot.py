# telegram dependencies
from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
# import my controller script and additional packadfe for logging to console
from kiwi_controller import *
# from model.questions import *
import logging

import collections
# log into console - very helpful  stuff
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')




class TelegramBot():
    # variable question needed for iteraction with a user & give additional
    # info how to search throw bot
    parameters_for_user_search = []
    result_of_search = []
    questions = ['city', 'city_to', 'data_f', 'data_t', 'passengers']

    def __init__(self):
        #  staff needed for start bot and register in telegram bot system
        self.updater = Updater(TELEGRAM_TOKEN)

        #  help to send message periodically,with  set intervals for messsaging
        # e.t.c . It runs asynchronously in a separate thread.
        job_q = self.updater.job_queue

        self.updater.dispatcher.add_handler(CommandHandler('search', self.handle_search))
        self.single_question = self.get_a_single_question()


    def start(self):
        self.updater.start_polling()
        self.updater.idle()
    # functions

    def create_handler_for_search(self):
        self.handler = MessageHandler(Filters.text | Filters.command, self.search)
        self.updater.dispatcher.add_handler(self.handler)

    def delete_search_handler(self):
        self.updater.dispatcher.remove_handler(self.handler)


    def get_a_single_question(self):
        yield from self.questions



    def iterate_through_questions(self, bot, update):
        # global single_question
        # global result_of_search
        try:
            question = next(self.single_question)

        except:
            single_question = self.get_a_single_question()
            print("-------------------" + str(self.parameters_for_user_search))
            # result_of_search = unpack_data(init_search_parameters(self.parameters_for_user_search[1], self.parameters_for_user_search[2]))
            self.result_of_search = init_search_parameters(self.parameters_for_user_search[1], self.parameters_for_user_search[2])
            print(self.result_of_search)
            self.send_updates_for_users(bot, update)
            self.result_of_search.clear()
            self.parameters_for_user_search.clear()  # empty list for futher use
            self.single_question = self.get_a_single_question()
            self.delete_search_handler()

            print("dsdssd" + " ".join(self.result_of_search))
            return
        return question

    def search(self, bot, update):
        self.parameters_for_user_search.append(update.message.text)
        message_for_user = self.iterate_through_questions(bot, update)
        try:
            bot.send_message(chat_id=CHAT_ID,
                             text=message_for_user)
        except:
            return

    def handle_search(self, bot, update):
        """Here we set handler to all text masseges and for invoke
        search command """
        self.create_handler_for_search()
        # updater.dispatcher.remove_handler(handler)
        self.search(bot, update)

    def send_updates_for_users(self, bot, job):
        couter = 25
        prev_counter = 0
        for it in range(0, int(len(self.result_of_search) / couter) + 1):
            if len(self.result_of_search) >= 25:
                bot.send_message(parse_mode='HTML', chat_id=CHAT_ID,
                                 text=f'''{''.join(self.result_of_search[prev_counter:couter])}''')
                prev_counter = couter
                couter *= 2
            else:
                bot.send_message(parse_mode='HTML', chat_id=CHAT_ID,
                                 text=f'''{''.join(self.result_of_search[1:10])}''')



# my_updates_sender = job_q.run_repeating(search, interval=90, first=0)


if __name__ == "__main__":
    t = TelegramBot()
    t.start()