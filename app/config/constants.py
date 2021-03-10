from telegram.ext import ConversationHandler

# State
RATE = '1'
END = ConversationHandler.END

USER_START_MESSAGING = 'Hi enter /help for detail'
SAY_GOODBYE = 'By By'
HELP = '''
Hi, to see the list of currencies enter / lst or / list\n
For convert money enter command - /exchange 'how much money' 'base rate' to 'exchange rate' 
(Ex: /exchange 10 USD to CAD)\n
To get a chart of currencies for the specified period, enter /history 'base rate'/'exchange rate' for 'count days' days
(Ex: /history USD/CAD for 7 days)\n
'''
