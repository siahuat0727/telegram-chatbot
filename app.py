# -*- coding: utf-8 -*-
import sys
from io import BytesIO
from try_database import Database
import telegram
from telegram.ext import Updater
from flask import Flask, request, send_file
from bs4 import BeautifulSoup
from urllib.request import urlopen
import random

from telegram.ext import CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from fsm import TocMachine

with open('token.txt') as f:
    API_TOKEN = f.readline().strip('\n')

WEBHOOK_URL = 'https://17fdba83.ngrok.io/hook'# input('url: ') + '/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)

db = Database()

all_kinds = ['politics', 'finance', 'entertainment', 'sports', 'society', 'local', 'world', 'lifestyle', 'health', 'technology', 'travel', 'odd']

machine = TocMachine(
    bot,
    states=[
        'state_initial',
        'state_news',
        'state_register',
        'state_favourite',
        'state2'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'state_initial',
            'dest': 'state_news',
            'conditions': 'is_going_to_state_news',
        },
        {
            'trigger': 'to_register',
            'source': 'state_initial',
            'dest': 'state_register',
        },
        {
            'trigger': 'to_news',
            'source': 'state_initial',
            'dest': 'state_news',
        },
        {
            'trigger': 'advance',
            'source': 'state_initial',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'select_favourite',
            'source': 'state_register',
            'dest': 'state_favourite'
        },
        {
            'trigger': 'to_news',
            'source': 'state_favourite',
            'dest': 'state_news',
        },
        {
            'trigger': 'advance',
            'source': 'state_news',
            'dest': 'state2',
        },
        {
            'trigger': 'go_back',
            'source': [
                'state_news',
                'state_register',
                'state_favourite',
                'state2'
            ],
            'dest': 'state_initial'
            # 'conditions' : 'leaving_state'
        }
    ],
    initial='state_initial',
    auto_transitions=False,
    show_conditions=True,
)

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


def state_initial_handler(update):
    chat_id = str(update.message.chat_id)
    if update.message.text == 'news':
        if db.exist(chat_id):
            update.message.reply_text('found chat_id')
            machine.to_news(update)
        else:
            update.message.reply_text('first time found ' + chat_id +' set username')
            machine.to_register(update)
    else:
        update.message.reply_text('try again')

def state_register_handler(update):
    text = get_text(update)
    db.insert(update.message.chat_id, text)
    update.message.reply_text('success set ' + text + ' as username')
    machine.select_favourite(update)

def state_news_handler(update):
    if update.message != None:
        if get_text(update) == 'exit':
            machine.go_back(update)
            return
        print('got message')
        scrape(update)
    elif update.callback_query != None:
        if update.callback_query.data == 'more':
            scrape(update.callback_query.chat_id)

def scrape(chat_id):
    base_url = "https://tw.news.yahoo.com/"
    total = 0
    dicts = {}
    for kind in all_kinds:
        n = db.select(chat_id, kind)
        total += n[0][0]
        dicts[kind] = n[0][0]
    print(dicts)

    mean = 8
    links_to_show = []

    for kind in all_kinds:
        choose = 0
        for i in range(mean):
            if random.uniform(0, 1) < dicts[kind]:
                choose += 1
        if choose > 0:
            url = base_url + kind
            html = urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(html, features='lxml')
            links = soup.find_all("a", {"class": "D(ib) Ov(h) Whs(nw) C($c-fuji-grey-l) C($c-fuji-blue-1-c):h Td(n) Fz(16px) Tov(e) Fw(700)"})
            links = [(link.get_text(), base_url + link['href']) for link in links]
            links_to_show += random.sample(links, choose)
    button_list = [
            [InlineKeyboardButton(t[0], url=t[1])] for t in links_to_show
    ]
    button_list.append([InlineKeyboardButton('more', callback_data='more')])
    reply_markup = InlineKeyboardMarkup(button_list)
    bot.send_message(chat_id=update.message.chat_id, text="hehe", reply_markup=reply_markup)

def state_favourite_handler(update):
    text = get_text(update)
    if text in all_kinds:
        update.message.reply_text('probability of ' + text + ' is added')
        db.update(get_chat_id(update), get_text(update), 2)
    elif get_text(update) == 'finish':
        machine.to_news(update)
    else:
        update.message.reply_text('please choose from keyboard button below')
    return

@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # print(update.message.from_user.username)
    if update.message != None:
        text = update.message.text
        update.message.reply_text('got it ' + text)
    globals()[machine.state + '_handler'](update)
    return 'ok'

@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

def get_chat_id(update):
    return update.message.chat_id

def get_text(update):
    return update.message.text

if __name__ == "__main__":
    _set_webhook()
    app.run()
