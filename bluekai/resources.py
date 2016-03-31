import flask
import logging
import json
import paramiko
import janrain_datalib
import janrain_datalib.exceptions
import janrain_datalib.utils
from . import bluekai_tsv
from .config import remote_filename
from .job import run as jobRunner
from .models import JobModel
from .sftpproxy import SftpProxy
from .date_utils import toRecordDateTime


def export():
    # must make a copy of the app config instead of accessing it directly
    # in the thread because the app and request contexts will be gone
    # by the time the thread runs
    config = flask.current_app.config.copy()

    logger = logging.getLogger(config['LOGGER_NAME'])

    _export(config, JobModel, SftpProxy, flask.current_app.threadexecutor, logger)

    return "ok", 200

def _export(config, JobModel, SftpProxy, threadexecutor, logger):
    job = JobModel.get(config)

    sftp = SftpProxy(paramiko, config, logger)
    writter = sftp.file(remote_filename(config), mode='w', bufsize=config['SFTP_BUFFER_SIZE'])

    if job.start():
        threadexecutor.submit(
            jobRunner, job, writter, config, logger,
            janrain_datalib, bluekai_tsv.fromRecord)
    else:
        logger.warning("export job already running")
