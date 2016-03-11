import flask
import logging
import janrain_datalib
import janrain_datalib.exceptions
import janrain_datalib.utils
import bluekai_tsv
from . import job
from .models import JobModel
from .sftpproxy import SftpProxy
from .records import recordsNewerThan


def export():
    # must make a copy of the app config instead of accessing it directly
    # in the thread because the app and request contexts will be gone
    # by the time the thread runs
    config = flask.current_app.config.copy()

    logger = logging.getLogger(config['LOGGER_NAME'])

    capture_app = janrain_datalib.get_app(
        config['JANRAIN_URI'],
        config['JANRAIN_CLIENT_ID'],
        config['JANRAIN_CLIENT_SECRET'])

    jobItem = JobModel.get(config)
    last_updated = jobItem.lastUpdated

    new_records_iterator = recordsNewerThan(capture_app, config, last_updated)

    sftp = SftpProxy(config, logger)
    writter = sftp.file(config['REMOTE_FILE'], mode='w', bufsize=config['SFTP_BUFFER_SIZE'])

    flask.current_app.threadexecutor.submit(
        job.run, JobModel, writter, config, logger, new_records_iterator, bluekai_tsv.fromRecord)

    return "ok", 200