def load_secret(key, default=None):
    key = key.upper()
    try:
        import secrets
        __dict__[key] = secrets.__dict__(key)
        print('INFO: Loaded {} from secrets'.format(key))
        return True
    except:
        try:
            import os
            __dict__[key] = os.environ[key]
            print('INFO: Loaded {} from ENV'.format(key))
            return True

        except:
            print('ERROR: {} not found, application may not work'.format(key))
    return False
        


load_secret('API_TOKEN')
load_secret('API_TOKEN')



DEFAULT_REPLY = "Sorry but I didn't understand you"
ERRORS_TO = 'bot-dev'

PLUGINS = [
    'panda_house.test',
]
