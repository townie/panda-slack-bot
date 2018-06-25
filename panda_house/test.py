from slackbot.bot import respond_to
from slackbot.bot import listen_to

from phue import Bridge

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



@respond_to('lights', re.IGNORECASE)
def lights(message):
	b = Bridge('192.168.1.16')

	# If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
	b.connect()
	lights = b.get_light_objects('id')

	message.reply(lights)
