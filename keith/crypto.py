# from six.moves.urllib import request
import json
import threading
import locale
import re

import requests
from slackbot import settings
from slackbot.bot import listen_to
from slackbot.bot import respond_to

from common import helper as cmn


@respond_to('mining stats', re.IGNORECASE)
def mining_stats(message):

    reply = ''

    stats = 'https://api.nicehash.com/api?method=stats.provider.ex&addr=' + \
        settings.NICEHASH_ADDRESS
    price = 'http://api.coindesk.com/v1/bpi/currentprice/'+settings.BITCOIN_FIAT+'.json'

    reqStats = requests.get(stats)

    stop_event = threading.Event()

    # parsing currency
    locale.setlocale(locale.LC_ALL, '')
    reqPrice = requests.get(price)

    priceCurrency = reqPrice.json()['bpi'][settings.BITCOIN_FIAT]['rate_float']

    reply += "\n\nUsing Currency: BTC/{0} = {1:,.2f}\n".format(
        settings.BITCOIN_FIAT, priceCurrency)
    reply += "=======================================\n"

    # parsing response
    cont = requests.get(stats).json()
    # cont = json.loads(rStats.decode('utf-8'))
    counter = 0
    balance = 0
    totalWorkers = 0
    totalProfitability = 0

    # parsing json
    for item in cont['result']['current']:
        counter += 1
        balance += float(item['data'][1])

        reply += "Algo: ({0}) {1}\n".format(item['algo'], item['name'])

        worker = 'https://api.nicehash.com/api?method=stats.provider.workers&addr=' + \
            settings.NICEHASH_ADDRESS+'&algo='+str(item['algo'])
        reqWorkers = requests.get(worker).json()
        totalWorkers += len(reqWorkers['result']['workers'])
        reply += "Workers: {0}\n".format(len(reqWorkers['result']['workers']))
        if (len(item['data'][0]) >= 1):
            profitability = float(item['profitability']) * \
                float(item['data'][0]['a'])

            reply += "Accepted Speed: {0} {1}/s\n".format(
                profitability, item['suffix'])
            reply += "Profitability: {0} BTC/day or {1:,.2f} {2}/day\n".format(
                profitability, profitability*priceCurrency, settings.BITCOIN_FIAT)
        else:
            reply += "Accepted Speed: 0 {0}/s\n".format(item['suffix'])
            reply += "Profitability: 0 BTC/day or 0.00 {0}/day\n".format(
                settings.BITCOIN_FIAT)

        if (len(reqWorkers['result']['workers']) >= 1):
            # import ipdb;ipdb.set_trace()

            totalProfitability += float(float(item['profitability'])
                                        * float(item['data'][0].get('a', 1)))
        reply += "Balance: {0} BTC or {1:,.2f} {2}\n".format(
            item['data'][1], float(item['data'][1])*priceCurrency, settings.BITCOIN_FIAT)
        reply += "---------------------------------------------------\n"

    reply += "===================================================\n"
    reply += "Total Algo: {}\n".format(counter)
    reply += "Total Workers: {0}\n".format(totalWorkers)
    reply += "Total Profitability: {0} BTC/day or {1:,.2f} {2}\n".format(
        profitability, float(profitability)*priceCurrency, settings.BITCOIN_FIAT)
    reply += "Total Balance: {} BTC\n".format(balance)

    message.reply(codeblock(reply))

def codeblock(s):
    return '```\n' + s + '```'
