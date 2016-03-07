"""Entry point for beanstalk to load the flask application."""
# must be named application for beanstalk to find it automatically
from bluekai import app as application

if __name__ == '__main__':
    application.run()
