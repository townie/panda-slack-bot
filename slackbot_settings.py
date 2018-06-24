try:
	import secrets

	API_TOKEN = secrets.API_TOKEN
except:
	print('ERROR: No Secrets were found')


DEFAULT_REPLY = "Sorry but I didn't understand you"
ERRORS_TO = 'bot-dev'

PLUGINS = [
    'panda_house.test',
]