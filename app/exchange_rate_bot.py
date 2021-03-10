import logging

from app.config.config import AppConfig
from app.handler import rate_conv_handler_kwargs

from telegram import Bot
from telegram.ext import Updater, ConversationHandler


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


class ExchangeRateBot:
    def __init__(self):
        self.token = AppConfig.BOT_TOKEN
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def setup(self):
        registered_user_conv_handler = ConversationHandler(**rate_conv_handler_kwargs)
        self.dispatcher.add_handler(registered_user_conv_handler)

    def run(self):
        self.updater.start_polling()
        self.updater.idle()

    @property
    def bot(self):
        return Bot(token=self.token)
