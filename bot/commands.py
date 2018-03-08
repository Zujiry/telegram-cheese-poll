from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


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
        
        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(done_handler)
        self.dispatcher.add_handler(echo_handler)
        # Must be added last
        self.dispatcher.add_handler(unknown_handler)
        
        ### Variables
        self.set_start = False
        self.set_options = False
        self.set_options_text = False
        self.options = []

    def start(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text="Let's create a new poll. First, send me the question.")
        self.set_start = True
        
    def echo(self, bot, update):
        if self.set_options:
            self.options.append(update.message.text)
        elif self.set_options_text:
            pass
        if self.set_start:
            bot.send_message(chat_id=update.message.chat_id, text='All the options please')
            self.set_options_text = True
            self.set_options = True
        else:
            bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    
    def done(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Creating your poll!")
        self.set_options = False
        self.set_start = False
        self.set_options_text = False
    
    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

    def run(self):
        self.updater.start_polling()


if __name__ == "__main__":
    bot = RoBoto()
    bot.run()
