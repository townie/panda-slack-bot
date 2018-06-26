import re
import json
import difflib


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
    b = Bridge('192.168.1.16', username=u'W0hrwByWt-KtIeYlqj0F9jL4eE6GvVK8ki62Akl8')

    # If the app is not registered and the button is not pressed, press the button and call
    # connect() (this only needs to be run a single time)
    b.connect()
    lights = b.get_light_objects('id')

    light_status = {light.name: light.on for light in lights.values()}

    message.reply(codeblock(convert_to_readable(light_status, headers=["Light", "Status"])))


@respond_to('turn (.*) (.*)', re.IGNORECASE)
def light_control(message, action, light):

    b = Bridge('192.168.1.16', username=u'W0hrwByWt-KtIeYlqj0F9jL4eE6GvVK8ki62Akl8')

    lights = b.get_light_objects('name')
    fuzzy_lights = {l.lower(): l for l in lights.keys()}

    found_key = ''
    if light.lower() in fuzzy_lights.keys():
        found_key = fuzzy_lights[light.lower()]
    else:
        possible = ifflib.get_close_matches(light.lower(), fuzzy_lights.keys())
        if len(possible) > 0:
            found_key = possible[0]
    if action == "off":
        lights[found_key].on = False
    elif action == "on":
        lights[found_key].on = True


def strbool(thing):
    if thing:
        return 'ON'
    return "OFF"


def codeblock(s):
    return '```\n' + s + '```'


def convert_to_readable(dictionary, headers=None):
    strout = ''

    if headers:
        strout = "{:<20} | {:<35}\n".format(headers[0], headers[1])

    strout += '-' * 40 + '\n'
    for k, v in dictionary.items():
        strout += "{:<20} | {:<35}\n".format(k, v)

    return strout


@respond_to('query (.*)', re.IGNORECASE)
def query(message, qstring):
    sf = Salesforce(password=settings.SFDC_PASSWORD, username=settings.SFDC_USERNAME,
                    security_token=settings.SFDC_SECURITY_TOKEN)

    out = sf.query(qstring)
    message.reply(json.dumps(out['records']))


@respond_to('panda', re.IGNORECASE)
def panda(message):

    message.reply("I LOVE PANDAS")
    message.react('panda_face')
    message.react('heart')
