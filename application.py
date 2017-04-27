"""Entry point for beanstalk to load the flask application."""
# must be named application for beanstalk to find it automatically
from bluekai import create_app
from bluekai import logging_init
from bluekai import get_config
from bluekai.models import JobModel

config = get_config()
application = create_app(config, JobModel)
logging_init(application)

if __name__ == '__main__':
    application.run()
