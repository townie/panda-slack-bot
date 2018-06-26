# import sys
# import os

from common.load_secret import load_secret

# slackbot settings
load_secret('API_TOKEN')  # slack token
load_secret('DEFAULT_REPLY', default='Try again.')
load_secret('ERRORS_TO', default='test')

# Salesforce
load_secret('SFDC_PASSWORD')
load_secret('SFDC_USERNAME')
load_secret('SFDC_SECURITY_TOKEN')

# Phillips Hue
load_secret('HUE_BRIDGE_IP')
load_secret('HUE_USERNAME')

# Mining
load_secret('NICEHASH_ADDRESS')
load_secret('BITCOIN_FIAT', default='USD')


# Plugins
PLUGINS = [
    'panda_house.house',
    'keith.crypto',
]
