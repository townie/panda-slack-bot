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
        return True
    except:
        try:
            __dict__[key] = os.environ[key]
            setattr(module, key, secrets.__dict__[key])

            print('INFO: Loaded {} from ENV'.format(key))
            key_set = True

        except:
            print('ERROR: {} not found, application may not work'.format(key))

    if not key_set and deault is not None:
        setattr(module, key, deault)
        key_set = True

    return key_set


load_secret('API_TOKEN')


DEFAULT_REPLY = "Sorry but I didn't understand you"
ERRORS_TO = 'bot-dev'

PLUGINS = [
    'panda_house.test',
]
