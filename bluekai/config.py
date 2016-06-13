"""Application configuration"""
import os
import json
from datetime import datetime

# environment variables and their defaults if not defined
_ENV_VARS = {
    'DEBUG': False,
    'APP_LOG_FILE': '/opt/python/log/application.log',
    'APP_LOG_FILESIZE': 10000000,
    'APP_LOG_NUM_BACKUPS': 20,
    'AWS_DEFAULT_REGION': '',
    'AWS_DYNAMODB_TABLE': '',
    'AWS_DYNAMODB_URL': '',
    'JANRAIN_URI': '',
    'JANRAIN_CLIENT_ID': '',
    'JANRAIN_CLIENT_SECRET': '',
    'JANRAIN_SCHEMA_NAME': 'user',
    'JANRAIN_BATCH_SIZE': 1000,
    'JANRAIN_ATTRIBUTE_KEYS': [],
    'REMOTE_HOST': '',
    'REMOTE_PORT': 22,
    'REMOTE_USERNAME': '',
    'REMOTE_PASSWORD': '',
    'REMOTE_RSA_KEY': '',
    'BLUEKAI_PARTNERNAME': '',
    'BLUEKAI_CLIENTNAME': '',
    'BLUEKAI_SITEID': '',
    'SFTP_BUFFER_SIZE': 32768,
}

def get_config():
    config = {}
    for key, default_value in _ENV_VARS.items():
        value = os.getenv(key, '')
        # empty string means use default value
        if value == '':
            value = default_value
        elif isinstance(_ENV_VARS[key], bool):
            if value.upper() != 'FALSE':
                value = True
            else:
                value = False
        elif isinstance(_ENV_VARS[key], int):
            try:
                value = int(value)
            except ValueError:
                value = default_value
        elif isinstance(_ENV_VARS[key], (dict, list)):
            try:
                value = json.loads(value)
            except ValueError:
                value = default_value
        config[key] = value
    return config

def remote_filename(config):

    partnerName = config.get('BLUEKAI_PARTNERNAME')
    clientName = config.get('BLUEKAI_CLIENTNAME')
    siteId = config.get('BLUEKAI_SITEID')
    extension = 'bz2'

    date = datetime.now().timestamp()

    if partnerName and clientName and siteId:
        data_filename = "{}_{}_{}_{}.{}".format(partnerName, clientName, siteId, date, extension)

    elif partnerName and siteId:
        data_filename = "{}_{}_{}.{}".format(partnerName, siteId, date, extension)

    trigger_filename = '{}.trigger'.format(data_filename)

    return (data_filename, trigger_filename)
