import urllib.request
import json
import threading
import locale


from slackbot import settings
from slackbot.bot import listen_to
from slackbot.bot import respond_to

@respond_to('mining stats', re.IGNORECASE)
def mining_stats(message):
    message.reply('I can understand hi or HI!')

    repy = ''

    stats = 'https://api.nicehash.com/api?method=stats.provider.ex&addr='+settings.NICEHASH_ADDRESS
    price = 'http://api.coindesk.com/v1/bpi/currentprice/'+settings.BITCOIN_FIAT+'.json'

    reqStats = urllib.request.Request(stats)

    stop_event = threading.Event()

    ##parsing currency
    locale.setlocale( locale.LC_ALL, '' )
    reqPrice = urllib.request.Request(price)
    rPrice = urllib.request.urlopen(reqPrice).read()
    priceCurrency=float(json.loads(rPrice)['bpi'][currency]['rate_float'])
    repy += "\n\nUsing Currency: BTC/{0} = {1:,.2f}".format(currency,priceCurrency)
    repy += "=======================================\n"

    ##parsing response
    rStats = urllib.request.urlopen(reqStats).read()
    cont = json.loads(rStats.decode('utf-8'))
    counter = 0
    balance = 0
    totalWorkers = 0
    profitability = 0

    ##parsing json
    for item in cont['result']['current']:
        counter += 1
        balance+=float(item['data'][1])

        repy += "Algo: ({0}) {1}\n".format(item['algo'],item['name'])


        worker = 'https://api.nicehash.com/api?method=stats.provider.workers&addr='+addr+'&algo='+str(item['algo'])
        reqWorkers = urllib.request.Request(worker)
        rWorker = urllib.request.urlopen(reqWorkers).read()
        totalWorkers += len(json.loads(rWorker)['result']['workers'])
        repy += "Workers: {0}\n".format(len(json.loads(rWorker)['result']['workers']))
        if (len(item['data'][0])>=1):
            repy += "Accepted Speed: {0} {1}/s\n".format(item['data'][0]['a'],item['suffix'])
            repy += "Profitability: {0} BTC/day or {1:,.2f} {2}/day\n".format(float(item['profitability'])*float(item['data'][0]['a']),float(item['profitability'])*float(item['data'][0]['a'])*priceCurrency, currency)
        else:
            repy += "Accepted Speed: 0 {0}/s\n".format(item['suffix'])
            repy += "Profitability: 0 BTC/day or 0.00 {0}/day\n".format(currency)


        if (len(json.loads(rWorker)['result']['workers'])>=1):
            profitability+=float(float(item['profitability'])*float(item['data'][0]['a']))
        repy += "Balance: {0} BTC or {1:,.2f} {2}\n".format(item['data'][1],float(item['data'][1])*priceCurrency, currency)
        repy += "---------------------------------------------------"

    repy += "==================================================="
    repy += "Total Algo: \n", counter
    repy += "Total Workers: {0}\n".format(totalWorkers)
    repy += "Total Profitability: {0} BTC/day or {1:,.2f} {2}\n".format(profitability, float(profitability)*priceCurrency, currency)
    repy += "Total Balance: ", balance, "BTC\n"