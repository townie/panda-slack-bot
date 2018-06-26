import sys
import os


def load_secret(key, default=None):
    """
    Set module level constant dynamically from secrets.py, env or default
    """
    key = key.upper()
    module = sys.modules[__name__]
    key_set = False

    try:
        import secrets
        setattr(module, key, secrets.__dict__[key])
        key_set = True
        print('INFO: Loaded {} from secrets'.format(key))
    except:
        try:
            setattr(module, key, os.environ[key])
            print('INFO: Loaded {} from ENV'.format(key))
            key_set = True
        except:
            print('ERROR: {} not found, application may not work'.format(key))

    if not key_set and default is not None:
        setattr(module, key, default)
        print('INFO: Used Default for {}.'.format(key))

        key_set = True

    return key_set

# slack token
load_secret('API_TOKEN')

# Salesforce
load_secret('SFDC_PASSWORD')
load_secret('SFDC_USERNAME')
load_secret('SFDC_SECURITY_TOKEN')

# Phillips Hue
load_secret('HUE_BRIDGE_IP')
load_secret('HUE_USERNAME')

# Mining
load_secret('NICEHASH_ADDRESS')
load_secret('BITCOIN_FIAT')

load_secret('DEFAULT_REPLY', default="Sorry but I didn't understand you")

load_secret('ERRORS_TO', default="test")


PLUGINS = [
    'panda_house.panda',
    'keith.crypto',

]
