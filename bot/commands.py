# -*- coding: utf-8 -*-

import os
import shlex

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
    m.update(bytes(x, encoding="utf-8"))
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
        start_handler = CommandHandler('start', self.start)
        done_handler = CommandHandler('done', self.done)
        unknown_handler = MessageHandler(Filters.command, self.unknown)
        echo_handler = MessageHandler(Filters.text, self.echo)
 
        self.dispatcher.add_handler(InlineQueryHandler(self.inline_handler))        
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(done_handler)
        self.dispatcher.add_handler(echo_handler)
        # Must be added last
        self.dispatcher.add_handler(unknown_handler)
        
        ### Variables
        self.pollname = ""
        self.set_start = False
        self.set_options = False
        self.set_options_text = False
        self.options = []

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Let's &lt;b&gt;create&lt;/b&gt; a new poll. First, send me the question.", parse_mode='HTML')
        bot.sendMessage(chat_id=update.message.chat_id, text="Let's <b>create</b> a new poll. First, send me the question.", parse_mode='HTML')
        self.set_start = True
        
    def echo(self, bot, update):
        if self.set_options:
            self.options.append(update.message.text)
        elif self.set_options_text:
            pass
        elif self.set_start:
            bot.send_message(chat_id=update.message.chat_id, text="All the options please")
            self.pollname = update.message.text
            self.set_options_text = True
            self.set_options = True
        else:
            bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    
    def done(self, bot, update):
        if self.set_start and self.set_options and self.set_options_text:
            bot.send_message(chat_id=update.message.chat_id, text="Creating your poll!")
            self.set_options = False
            self.set_start = False
            self.set_options_text = False
            
            query_id = update.chosen_inline_result.result_id
            
            options = [
                Option(id=query_id + hash(part)[:32], title=self.pollname) for option in self.options
            ]
        
            poll = Poll(
                id=query_id,
                title=self.pollname,
                creator_id=update.message.chat_id,
                options=options
            )
            db_session.add(poll)
            db_session.commit()
            bot.send_message(chat_id=update.message.chat_id, text=str("Poll saved!"))
        else:
            bot.send_message(chat_id=update.message.chat_id, text="You first have to create a poll via typing /start")
    
    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def run(self):
        self.updater.start_polling()
    
    def inline_handler(self, bot, update):
        query = update.inline_query.query

        if query == '':
            return

        try:
            parts = shlex.split(query)
        except ValueError as e:
            return

        query_id = update.inline_query.id

        if len(parts) == 1:
            update.inline_query.answer([
                InlineQueryResultArticle(
                    id=query_id,
                    title=parts[0],
                    input_message_content=InputTextMessageContent(
                        "*{}*".format(parts[0]), parse_mode="markdown"))
            ])
        else:
            options = deduplicate(parts[1:])
            description = " / ".join(options)

            buttons = generate_buttons(query_id, options)
            update.inline_query.answer([
                InlineQueryResultArticle(
                    id=query_id,
                    title=parts[0],
                    description=description,
                    input_message_content=InputTextMessageContent(
                    generate_message(parts[0], options),
                    parse_mode="markdown"),
                    reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))
            ])

if __name__ == "__main__":
    bot = RoBoto()
    bot.run()
