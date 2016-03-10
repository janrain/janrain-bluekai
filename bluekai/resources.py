import flask
import logging
import janrain_datalib
import janrain_datalib.exceptions
import janrain_datalib.utils
import bluekai_tsv
from pynamodb.exceptions import DoesNotExist
from .date_utils import fromRecordDateTime
from .date_utils import toRecordDateTime
from .date_utils import fromModelDateTime
from .date_utils import toModelDateTime
from .models import Model
from .models import loadLastUpdated
from .models import saveLastUpdated
from .sftpproxy import SftpProxy

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

    last_updated = loadLastUpdated(Model, config)

    new_records_iterator = recordsNewerThan(capture_app, config, last_updated)

    sftp = SftpProxy(config, logger)
    with sftp.file(config['REMOTE_FILE'], mode='w', bufsize=config['SFTP_BUFFER_SIZE']) as fp:

        record_num = 0
        for record_num, record in enumerate(new_records_iterator, start=1):

            record_last_updated = fromRecordDateTime(record['lastUpdated'])
            if record_last_updated > last_updated:
                last_updated = record['lastUpdated']
                saveLastUpdated(Model, config,lastUpdated)

            row = bluekai_tsv.fromRecord(record)

            # write to remote file
            fp.write(row)

            if record_num % config['JANRAIN_BATCH_SIZE'] == 0:
                logger.debug("wrote record {}".format(record_num))

        logger.info("exported {} records".format(record_num))


def recordsNewerThan(capture_app, config, date):

    capture_schema = capture_app.get_schema(config['JANRAIN_SCHEMA_NAME'])

    records_iterator = capture_schema.records.iterator(
        filtering="lastUpdated > '{}'".format(date.strftime("%Y-%m-%d %H:%M:%S.%f")),
        batch_size=config['JANRAIN_BATCH_SIZE']
    )

    return records_iterator

def newestLastUpdated(records):
    datetimes = map(lambda each: fromRecordDateTime(each['lastUpdated']), records)
    if len(datetimes):
        return max(datetimes)
    else:
        return None
