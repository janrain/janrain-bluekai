import flask
import logging
import json
import paramiko
import janrain_datalib
import janrain_datalib.exceptions
import janrain_datalib.utils
from . import bluekai_tsv
from .job import run as jobRunner
from .models import JobModel
from .sftpproxy import SftpProxy
from .date_utils import toRecordDateTime
from .bluekai_writer import BlueKaiWriter


def export():
    # must make a copy of the app config instead of accessing it directly
    # in the thread because the app and request contexts will be gone
    # by the time the thread runs
    config = flask.current_app.config.copy()

    logger = logging.getLogger(config['LOGGER_NAME'])

    _export(config, JobModel, SftpProxy, BlueKaiWriter, flask.current_app.threadexecutor, logger)

    return "ok", 200

def _export(config, JobModel, SftpProxy, Writer, threadexecutor, logger):
    job = JobModel.get(config)

    sftp = SftpProxy(paramiko, config, logger)
    writerFactory = lambda: Writer(sftp, config)

    if job.start():
        threadexecutor.submit(
            jobRunner, job, writerFactory, config, logger,
            janrain_datalib, bluekai_tsv.fromRecord)
    else:
        logger.warning("export job already running")
