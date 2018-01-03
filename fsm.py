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
        update.message.reply_text("I'm entering state_news")
        button_list = [
                [InlineKeyboardButton('col', callback_data='callback__')]
        ]
        reply_markup = InlineKeyboardMarkup(button_list)
        self.bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)

    def on_exit_state_news(self, update):
        update.message.reply_text('Leaving state_news')

    def is_going_to_state_register(self, update):
        text = update.message.text
        return self.state == 'user' and text.lower() == 'register'

    def on_enter_state_register(self, update):
        update.message.reply_text("I'm entering state_register")

        button_list=[
            [
                KeyboardButton('newws')
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(button_list)
        self.bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)
        # self.select_favourite(update)

    def on_exit_state_register(self, update):
        update.message.reply_text('Leaving state_register')




    def is_going_to_state_favourite(self, update):
        text = update.message.text
        return self.state == 'register' and text.lower() == 'favourite'

    def on_enter_state_favourite(self, update):
        update.message.reply_text("I'm entering state_favourite")
        button_list=[
            [KeyboardButton(s) for s in ['politics', 'finance', 'entertainment', 'sports', 'society', 'local', 'world', 'lifestyle', 'health', 'technology', 'travel', 'odd']]
        ]
        reply_markup = ReplyKeyboardMarkup(button_list)
        self.bot.send_message(chat_id=update.message.chat_id, text="A two-column menu", reply_markup=reply_markup)

    def on_exit_state_favourite(self, update):
        update.message.reply_text('Leaving state_favourite')




    def is_going_to_state2(self, update):
        text = update.message.text
        return text.lower() == 'go to state2'

    def on_enter_state2(self, update):
        update.message.reply_text("I'm entering state2")
        self.go_back(update)

    def on_exit_state2(self, update):
        update.message.reply_text('Leaving state2')
