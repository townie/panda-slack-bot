import sys
import os


def load_secret(key, default=None, module_name=None):
    """
    Set module level constant dynamically from secrets.py, env or default
    """
    if module_name is None:
        module_name = 'slackbot_settings'

    key = key.upper()
    module = sys.modules[module_name]
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
