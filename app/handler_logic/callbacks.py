from telegram import Update
from telegram.ext import CallbackContext

from app.handler_logic.presenters import (
    StartPresenter,
    CancellationPresenter,
    GetRateListPresenter,
    ExchangeMoneyPresenter,
    HistoryRatePresenter
)


def start(update: Update, context: CallbackContext) -> int:
    start_presenter = StartPresenter(update, context)
    start_presenter.present_response()
    return start_presenter.next_state


def cancel(update: Update, context: CallbackContext) -> int:
    cancellation_presenter = CancellationPresenter(update)
    cancellation_presenter.present_response()
    return cancellation_presenter.next_state


def get_rate_list(update: Update, context: CallbackContext) -> int:
    cancellation_presenter = GetRateListPresenter(update)
    cancellation_presenter.present_response()
    return cancellation_presenter.next_state


def exchange_money(update: Update, context: CallbackContext) -> int:
    cancellation_presenter = ExchangeMoneyPresenter(update, context)
    cancellation_presenter.present_response()
    return cancellation_presenter.next_state


def history_rate(update: Update, context: CallbackContext) -> int:
    cancellation_presenter = HistoryRatePresenter(update, context)
    cancellation_presenter.present_response()
    return cancellation_presenter.next_state
