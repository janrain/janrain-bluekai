import flask
import logging
import json
import janrain_datalib
import janrain_datalib.exceptions
import janrain_datalib.utils
import bluekai_tsv
from .job import run as jobRunner
from .models import JobModel
from .sftpproxy import SftpProxy
from .records import recordsNewerThan
from .date_utils import toRecordDateTime


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

    job = JobModel.get(config)
    last_updated = job.lastUpdated

    new_records_iterator = recordsNewerThan(capture_app, config, last_updated)

    sftp = SftpProxy(config, logger)
    writter = sftp.file(config['REMOTE_FILE'], mode='w', bufsize=config['SFTP_BUFFER_SIZE'])

    if job.start():
        flask.current_app.threadexecutor.submit(
            jobRunner, JobModel, writter, config, logger,
            new_records_iterator, bluekai_tsv.fromRecord)
    else:
        logger.warning("export job already running")

    return json.dumps({
            "started": job.started and toRecordDateTime(job.started),
            "ended": job.ended and toRecordDateTime(job.ended),
            "running": job.running,
            "lastUpdated": job.lastUpdated and toRecordDateTime(job.lastUpdated),
            "error": job.error,
        })
