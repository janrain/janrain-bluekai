"""Flask application setup."""
import concurrent.futures
import flask
import logging
import logging.handlers
from .config import get_config
#from .actions import sync
from ._version import __version__


def create_app(config):
  app = flask.Flask(__name__)
  app.config.update(config)

  # add routes
  app.add_url_rule('/', 'root', lambda: 'ok')

  # add the thread executor to the app
  app.threadexecutor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

  @app.after_request
  def add_headers(response):
      """additional headers for each response"""
      response.headers['X-App-Version'] = __version__
      return response

  return app

def logging_init(app):
  # setup logging
  handler = logging.handlers.RotatingFileHandler(
      app.config['APP_LOG_FILE'],
      backupCount=app.config['APP_LOG_NUM_BACKUPS'],
      maxBytes=app.config['APP_LOG_FILESIZE'])

  if app.debug:
      handler.setLevel(logging.DEBUG)
  else:
      handler.setLevel(logging.INFO)

  msg_format = '[%(asctime)s] %(levelname)s: %(message)s'
  timestamp_format = '%Y-%m-%d %H:%M:%S %z'
  formatter = logging.Formatter(msg_format, timestamp_format)
  handler.setFormatter(formatter)
  logger = logging.getLogger(app.config['LOGGER_NAME'])
  logger.addHandler(handler)
  logger.setLevel(logging.DEBUG)

  return handler
