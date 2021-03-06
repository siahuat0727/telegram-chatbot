from transitions.extensions import GraphMachine
from telegram import *

class TocMachine(GraphMachine):
    def __init__(self, bot, **machine_configs):
        self.bot = bot
        self.machine = GraphMachine(
            model = self,
            **machine_configs
        )

    def is_going_to_state_news(self, update):
        text = update.message.text
        return (self.state == 'user' or self.state == 'state_register') and text.lower() == 'news'

    def before_entering_state_news(self, update):
        self.first_use(update)

    def on_enter_state_news(self, update):
        # update.message.reply_text("I'm entering state_news")
        return

    def on_exit_state_news(self, update):
        # update.message.reply_text('Leaving state_news')
        return

    def is_going_to_state_register(self, update):
        text = update.message.text
        return self.state == 'user' and text.lower() == 'register'

    def on_enter_state_register(self, update):
        return
        # update.message.reply_text("I'm entering state_register")
        # self.select_favourite(update)

    def on_exit_state_register(self, update):
        return
        # update.message.reply_text('Leaving state_register')




    def is_going_to_state_favourite(self, update):
        text = update.message.text
        return self.state == 'register' and text.lower() == 'favourite'

    def on_enter_state_favourite(self, update):
        # update.message.reply_text("I'm entering state_favourite")
        button_list=[
            [KeyboardButton(s)] for s in ['politics', 'finance', 'entertainment', 'sports', 'society', 'local', 'world', 'lifestyle', 'health', 'technology', 'travel', 'odd', 'finish']
        ]
        reply_markup = ReplyKeyboardMarkup(button_list)
        self.bot.send_message(chat_id=update.message.chat_id, text="Please select the topic you interest in", reply_markup=reply_markup)

    def on_exit_state_favourite(self, update):
        # update.message.reply_text('Leaving state_favourite')
        return
