# -*- coding: utf-8 -*-

import os
import hashlib
import shlex

from telegram import KeyboardButton, ReplyKeyboardMarkup

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ChosenInlineResultHandler, InlineQueryHandler, Updater

from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, Float
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# os.environ["DB_URL"]
engine = create_engine('sqlite:////home/telegram-cheese-poll/bot.db', echo=True)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def hash(x):
    m = hashlib.sha256()
    m.update(str(x))
    return m.hexdigest()


class Poll(Base):
    __tablename__ = 'polls'
    id = Column(BigInteger, primary_key=True)
    title = Column(String)
    creator_id = Column(BigInteger)
    options = relationship("Option")


class Option(Base):
    __tablename__ = 'options'
    id = Column(String, primary_key=True)
    title = Column(String)
    poll_id = Column(BigInteger, ForeignKey('polls.id'))
    poll = relationship("Poll", back_populates="options")


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Float, primary_key=True)
    user_id = Column(BigInteger, primary_key=True)
    option_id = Column(String, primary_key=True)


Base.metadata.create_all(bind=engine)


### Functions
class RoBoto():

    def __init__(self):
        self.updater = Updater(token='325958539:AAF4OdXPaS_TL7JR3fVtDrzh_Kxx34Kx54w')
        self.dispatcher = self.updater.dispatcher

        ### Handler
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CommandHandler('done', self.done))
        self.dispatcher.add_handler(CommandHandler('stop', self.stop))
        self.dispatcher.add_handler(MessageHandler(Filters.text, self.echo))
        # Must be added last
        self.dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

        ### Variables
        self.pollname = ""
        self.set_start = False
        self.set_options = False
        self.set_options_text = False
        self.options = []

    def start(self, bot, update):
        message = "Let's create a new poll. First, send me the question."
        bot.sendMessage(chat_id=update.message.chat_id, text=message)
        self.set_start = True

    def echo(self, bot, update):
        if self.set_options:
            self.options.append(update.message.text)
            # bot.editMessageText(message_id=self.response['message_id'], chat_id=self.response['chat']['id'],
            #                    text='its another option')
        elif self.set_options_text:
            pass
        elif self.set_start:
            self.response = bot.send_message(chat_id=update.message.chat_id, text="All the options please")
            self.pollname = update.message.text
            self.set_options_text = True
            self.set_options = True
        else:
            bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

    def done(self, bot, update):
        if self.set_start and self.set_options and self.set_options_text:
            self.set_options = False
            self.set_start = False
            self.set_options_text = False

            '''
            options = [
                Option(id=str(update.message.chat_id) + str(hash(30)[:32]), title=self.pollname) for option in
                self.options
            ]

            poll = Poll(
                id=hash(30),
                title=self.pollname,
                creator_id=update.message.chat_id,
                options=options
            )
            db_session.add(poll)
            db_session.commit()
            '''
            bot.send_message(chat_id=update.message.chat_id, text=str("Created your poll!"))
            buttons = []
            for option in self.options:
                buttons.append([
                    InlineKeyboardButton(text=option,
                                         callback_data=option),
                    InlineKeyboardButton(text='Nein',
                                         callback_data=option + " Nein")
                ])

            bot.send_message(chat_id=update.message.chat_id, text=self.pollname,
                             reply_markup=InlineKeyboardMarkup(buttons))
            self.options = []
        else:
            bot.send_message(chat_id=update.message.chat_id, text="You first have to create a poll via typing /start")

    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def run(self):
        self.updater.start_polling()

    def stop(self, bot, update):
        self.updater.idle()


if __name__ == "__main__":
    bot = RoBoto()
    bot.run()
