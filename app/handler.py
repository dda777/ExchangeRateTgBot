from telegram.ext import CommandHandler, Handler

from app.handler_logic.callbacks import (
    start,
    cancel,
    get_rate_list,
    exchange_money,
    history_rate,
    get_help,
)
from app.config.constants import RATE


entry_point_start: Handler = CommandHandler('start', start)
fallback_cancel: Handler = CommandHandler('stop', cancel)
get_help_handler: Handler = CommandHandler('help', get_help)
get_rate_list_handler: Handler = CommandHandler(['lst', 'list'], get_rate_list)
exchange_money_handler: Handler = CommandHandler('exchange', exchange_money, pass_args=True)
history_rate_handler: Handler = CommandHandler('history', history_rate, pass_args=True)

rate_conv_handler_kwargs = {
    'entry_points': [
        entry_point_start
    ],
    'states': {
        RATE: [get_rate_list_handler, exchange_money_handler, history_rate_handler, get_help_handler],
    },
    'fallbacks': [fallback_cancel],
}
