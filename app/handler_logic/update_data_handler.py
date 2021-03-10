from abc import ABCMeta, abstractmethod

from telegram import Update
from telegram.ext import CallbackContext


class BaseUpdateDataHandler(metaclass=ABCMeta):
    def __init__(self, update: Update, context: CallbackContext):
        self._update = update
        self._context = context

    @abstractmethod
    def handle_data(self):
        raise NotImplementedError
