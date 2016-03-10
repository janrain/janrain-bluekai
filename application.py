"""Entry point for beanstalk to load the flask application."""
# must be named application for beanstalk to find it automatically
from bluekai import create_app
from bluekai import logging_init
from bluekai import get_config
from bluekai.models import Model

if __name__ == '__main__':
    config = get_config()
    application = create_app(config, Model)
    logging_init(application)
    application.run()
