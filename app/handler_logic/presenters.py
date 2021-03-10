from typing import Union
from abc import ABCMeta, abstractmethod
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InputMediaPhoto
from telegram.ext import CallbackContext, ConversationHandler
from requests import get
from app.config import constants
from app.config.config import AppConfig
from app.database.database import DataBase
from datetime import datetime, timedelta
import os
import matplotlib.pyplot as plt


class TelegramPresenter(metaclass=ABCMeta):
    def __init__(self, update: Update, context: CallbackContext = None):
        self._update = update
        self._context = context

    def present_response(self):
        self._update.message.reply_text(
            text=self.text,
            reply_markup=self.reply_keyboard
        )

    @abstractmethod
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        raise NotImplementedError

    @abstractmethod
    def text(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def next_state(self) -> int:
        raise NotImplementedError


class StartPresenter(TelegramPresenter):
    def __init__(self, update: Update, context: CallbackContext):
        super().__init__(update, context)

    @property
    def text(self) -> str:
        return constants.USER_START_MESSAGING

    @property
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        return ReplyKeyboardRemove()

    @property
    def next_state(self):
        return constants.RATE


class CancellationPresenter(TelegramPresenter):
    def __init__(self, update: Update):
        super().__init__(update)

    @property
    def text(self) -> str:
        return constants.SAY_GOODBYE

    @property
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        return ReplyKeyboardRemove()

    @property
    def next_state(self) -> int:
        return ConversationHandler.END


class ExchangeMoneyPresenter(TelegramPresenter):
    def __init__(self, update: Update, context: CallbackContext):
        super().__init__(update, context)
        self.rate_data = self.get_rate_data()['rates']

    def validate(self):
        if (
                self._context.args[0].isdigit() and
                self._context.args[1] in [*self.rate_data] and
                self._context.args[3] in [*self.rate_data] and
                self._context.args[2] == 'to'
        ):
            return True
        else:
            return False

    def convert_currency(self):
        if self.validate():
            data = self.get_rate_data(self._context.args[1])['rates']
            value = int(self._context.args[0]) * data[self._context.args[3]]
            return f'{self.to_fixed(value, 2)} - {self._context.args[3]}'
        return 'Error'

    @staticmethod
    def to_fixed(num_obj, digits=0):
        return f"{num_obj:.{digits}f}"

    @staticmethod
    def get_rate_data(base='USD'):
        return get(AppConfig.RATE_API_LINK+base).json()

    @property
    def text(self) -> str:
        return self.convert_currency()

    @property
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        return ReplyKeyboardRemove()

    @property
    def next_state(self) -> int:
        return constants.RATE


class HistoryRatePresenter(TelegramPresenter):
    def __init__(self, update: Update, context: CallbackContext):
        super().__init__(update, context)
        print(self._context.args)
        self.history_rate = self.get_history_rate_data()

    def validate(self):
        if (
                self._context.args[2].isdigit() and
                self._context.args[1] == 'for' and
                self._context.args[3] == 'days'
        ):
            return True
        else:
            return False


    def get_history_rate_data(self):
        base,  symbols = self._context.args[0].split('/')
        start_at = datetime.now() - timedelta(days=int(self._context.args[2]))
        end_at = str(datetime.now().date())
        current_dict = get(AppConfig.RATE_HISTORY_API_LINK+base+'&start_at='+str(start_at.date())+'&end_at='+end_at+'&symbols='+symbols).json()['rates']
        keylist = list(current_dict.keys())
        keylist.sort()
        new_dict = {}
        for key in keylist:
            new_dict.update({key: current_dict[key]})
        return new_dict

    def generate_chart(self):
        x = []
        y = []
        for value in self.history_rate:
            x.append(value)
            y.append(self.history_rate[value][self._context.args[0].split('/')[1]])
        fig, ax = plt.subplots()
        ax.plot(x, y, color="g")
        plt.grid()
        plt.savefig('chart.png')

    @property
    def text(self) -> str:
        self.generate_chart()
        photo = [InputMediaPhoto(media=open('chart.png', 'rb'))]
        self._update.effective_user.bot.send_media_group(self._update.effective_user.id, media=photo)
        return ''


    @property
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        return ReplyKeyboardRemove()

    @property
    def next_state(self) -> int:
        return constants.RATE


class GetRateListPresenter(TelegramPresenter):
    def __init__(self, update: Update):
        super().__init__(update)
        self.data_base = DataBase('rate.yaml')
        self._user_id = self._update.effective_user.id

    @staticmethod
    def get_rate_data(base='USD'):
        return get(AppConfig.RATE_API_LINK+base).json()

    def save_rate_data(self, data):
        current_date = {'date': datetime.now()}
        self.data_base.dump_data({self._user_id: [data, current_date]})

    def load_rate_data(self):
        data = self.data_base.load_data()
        if self.check_elapsed_time(data[self._user_id][1]['date']):
            return data[self._user_id][0]
        else:
            current_date = {'date': datetime.now()}
            data[self._user_id] = [self.get_rate_data()['rates'], current_date]
            self.data_base.dump_data(data)
            return data[self._user_id][0]


    @staticmethod
    def check_elapsed_time(time):
        return True if time + timedelta(minutes=10) > datetime.now() else False

    def data_exist(self):
        return True if self.data_base.load_data() else False

    @property
    def text(self) -> str:
        output = ''
        if self.data_exist():
            rate_data = self.load_rate_data()
        else:
            rate_data = self.get_rate_data()['rates']
            self.save_rate_data(rate_data)

        for val in rate_data:
            output += f"{val}: {rate_data[val]}\n"
        return output

    @property
    def reply_keyboard(self) -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
        return ReplyKeyboardRemove()

    @property
    def next_state(self) -> int:
        return constants.RATE
