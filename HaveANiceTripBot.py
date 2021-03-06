# telegram dependencies
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from threading import Thread

# import my controller script and additional packadfe for logging to console
from kiwi_controller import *
# from model.questions import *
import logging

import collections

# log into console - very helpful  stuff
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Test():
    parameters_for_user_search = []






class TelegramBot():
    # variable question needed for iteraction with a user & give additional
    # info how to search throw bot

    questions = [
        'Вкажіть пункт відправлення.Вживайте лише англійські назви міст без спеціальних знаків (наприклад: Krakow).',
        'Тепер вкажіть місто прибуття. Вживайте лише англійські назви міст без спеціальних знаків(наприклад: Kiev).',
        'Хороший вибір! Тепер вкажіть від якої дати шукати  в форматі 10/09/2018',
        ' Тепер вкажіть до якої дати шукати  в форматі 23/11/2018', 'Вкажіть кількість пасажирів. Наприклад 2']

    def __init__(self):
        #  staff needed for start bot and register in telegram bot system
        self.updater = Updater(TELEGRAM_TOKEN)
        self.parameters_for_user_search = []
        self.result_of_search = []
        #  help to send message periodically,with  set intervals for messsaging
        # e.t.c . It runs asynchronously in a separate thread.
        job_q = self.updater.job_queue

        self.updater.dispatcher.add_handler(CommandHandler('search', self.handle_search))

    def start(self):
        self.updater.start_polling()
        self.updater.idle()

    def cleanup_variables(self):
        self.result_of_search = []
        self.parameters_for_user_search = []  # empty list for futher use
        self.delete_search_handler()

    # functions

    def create_handler_for_search(self):
        self.handler = MessageHandler(Filters.text | Filters.command, self.search)
        self.updater.dispatcher.add_handler(self.handler)

    def delete_search_handler(self):
        self.updater.dispatcher.remove_handler(self.handler)

    def get_a_single_question(self):
        yield from self.questions

    def iterate_through_questions(self, bot, update, parameters_for_user_searc):
        global sorted_data
        # global result_of_search

        parameters_for_user_search = parameters_for_user_searc
        parameters_for_user_search.append("") if update.message.text == '-' else parameters_for_user_search.append(
            update.message.text)
        try:
            question = next(self.single_question)


        except:
            self.single_question = self.get_a_single_question()
            print("-------------------" + str(self.parameters_for_user_search))
            try:
                self.result_of_search = init_search_parameters(parameters_for_user_search[1],
                                                               parameters_for_user_search[2],
                                                               # self.parameters_for_user_search[3],
                                                               # self.parameters_for_user_search[4],
                                                               # self.parameters_for_user_search[5]
                                                               )
            except:
                self.cleanup_variables()
                parameters_for_user_search = []

            try:
                self.send_updates_for_users(bot, update)
            except:
                print("____________________ERROR IN SEND MESSAGE____________________")
            finally:
                self.cleanup_variables()
            return
        return question

    def search(self, bot, update, a=[]):
        message_for_user = self.iterate_through_questions(bot, update, a)
        try:
            bot.send_message(chat_id=update.message.chat_id,
                             text=message_for_user)
        except:
            return

    def handle_search(self, bot, update):
        """Here we set handler to all text masseges and for invoke
        search command """
        self.create_handler_for_search()
        # updater.dispatcher.remove_handler(handler)

        self.single_question = self.get_a_single_question()
        self.search(bot, update)

    def send_updates_for_users(self, bot, update):
        couter = 25
        prev_counter = 0
        print(update.message.chat_id, CHAT_ID)
        for it in range(0, int(len(self.result_of_search) / couter) + 1):
            if len(self.result_of_search) >= 25:
                bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,
                                 text=f'''{''.join(self.result_of_search[prev_counter:couter])}''')
                prev_counter = couter
                couter *= 2
            else:
                bot.send_message(parse_mode='HTML', chat_id=update.message.chat_id,
                                 text=f'''{''.join(self.result_of_search[1:10])}''')




# my_updates_sender = job_q.run_repeating(search, interval=90, first=0)
if __name__ == "__main__":
    t = TelegramBot()
    t.start()
