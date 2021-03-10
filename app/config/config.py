from decouple import config


class AppConfig:
    BOT_TOKEN = config('BOT_TOKEN')
    RATE_API_LINK = config('RATE_API_LINK')
    RATE_HISTORY_API_LINK = config('RATE_HISTORY_API_LINK')
