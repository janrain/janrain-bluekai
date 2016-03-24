"""Application configuration"""
import os

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
    'JANRAIN_ATTRIBUTE_KEYS': "",
    'REMOTE_HOST': '',
    'REMOTE_PORT': 22,
    'REMOTE_USERNAME': '',
    'REMOTE_PASSWORD': '',
    'REMOTE_RSA_KEY': '',
    'REMOTE_FILE': 'janrain-bluekai.tsv',
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
        config[key] = value
    return config
