import re
import json

from phue import Bridge
from simple_salesforce import Salesforce
from slackbot import settings
from slackbot.bot import listen_to
from slackbot.bot import respond_to


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


@respond_to('query (.*)', re.IGNORECASE)
def query(message, qstring):
    sf = Salesforce(password=settings.SFDC_PASSWORD, username=settings.SFDC_USERNAME,
                    security_token=settings.SFDC_SECURITY_TOKEN)

    out = sf.query(qstring)
    message.reply(json.dumps(out['records']))


@respond_to('panda', re.IGNORECASE)
def panda(message):

    message.reply("I LOVE PANDAS")
