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
    b = Bridge(settings.HUE_BRIDGE_IP, username=settings.HUE_USERNAME)
    # If the app is not registered and the button is not pressed, press the
    # button and call connect() (this only needs to be run a single time)
    lights = b.get_light_objects('id')

    light_status = {
        light.name: lightbool(light.on)
        for light in lights.values()
    }

    res = codeblock(convert_to_table(light_status, headers=["Light", "Status"]))
    message.reply(res)


@respond_to('turn (.*) (.*)', re.IGNORECASE)
def light_control(message, action, light):

    b = Bridge(settings.HUE_BRIDGE_IP, username=settings.HUE_USERNAME)

    lights = b.get_light_objects('name')
    fuzzy_lights = {l.lower(): l for l in lights.keys()}

    # key search
    found_key = ''
    if light.lower() in fuzzy_lights.keys():
        found_key = fuzzy_lights[light.lower()]
    else:
        possible = difflib.get_close_matches(
            light.lower(), fuzzy_lights.keys())
        if len(possible) > 0:
            found_key = fuzzy_lights[possible[0]]

    # control action
    if action == "off" and found_key in lights:
        lights[found_key].on = False
        message.react('bulbout')
    elif action == "on" and found_key in lights:
        lights[found_key].on = True
        message.react('bulb')
    else:
        message.react('bulbunknown')


@respond_to('query (.*)', re.IGNORECASE)
def query(message, qstring):
    sf = Salesforce(password=settings.SFDC_PASSWORD,
                    username=settings.SFDC_USERNAME,
                    security_token=settings.SFDC_SECURITY_TOKEN)

    out = sf.query(qstring)
    message.reply(json.dumps(out['records']))


@respond_to('panda', re.IGNORECASE)
def panda(message):
    message.reply("I LOVE PANDAS")
    message.react('panda_face')
    message.react('heart')


def lightbool(thing):
    if thing:
        return 'ON'
    return "OFF"


def codeblock(s):
    return '```\n' + s + '```'


def convert_to_table(dictionary, headers=None):
    strout = ''

    if headers:
        strout = "{:<20} | {:<35}\n".format(headers[0], headers[1])

    strout += '-' * 40 + '\n'
    for k, v in dictionary.items():
        strout += "{:<20} | {:<35}\n".format(k, v)

    return strout
