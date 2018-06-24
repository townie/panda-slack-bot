from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re

@respond_to('hi', re.IGNORECASE)
def hi(message):
    message.reply('I can understand hi or HI!')
    # react with thumb up emoji
    message.react('+1')


@respond_to('status', re.IGNORECASE)
def status(message):
	message.reply('WORK IN PROGRESS')
	message.react('construction_worker')