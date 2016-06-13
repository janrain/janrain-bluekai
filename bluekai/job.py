from contextlib import closing
from .date_utils import fromRecordDateTime
from .date_utils import toRecordDateTime
from .records import recordsNewerThan

def run(job, writerFactory, config, logger, datalib, converter):

    logger.info("start")

    exception = None

    try:

        do_job(job, writerFactory, config, logger, datalib, converter)

    except Exception as catch_exception:

        exception = catch_exception

    finally:
        if exception:
            error = str(exception)
            job.error = error
            logger.error(error)
            if config['DEBUG']:
                logger.exception(exception)
        # update db regardless
        job.stop()
        logger.info("end ({} seconds)".format(job.ended - job.started))

def do_job(job, writerFactory, config, logger, datalib, converter):

    last_updated = job.lastUpdated

    capture_app = datalib.get_app(
        config['JANRAIN_URI'],
        config['JANRAIN_CLIENT_ID'],
        config['JANRAIN_CLIENT_SECRET'])

    records_iterator = recordsNewerThan(capture_app, config, last_updated)

    output = ""
    record_num = 0
    for record_num, record in enumerate(records_iterator, start=1):

        try:
            row = converter(record, config['JANRAIN_ATTRIBUTE_KEYS'])
        except TypeError as exception:
            message = str(exception)
            logger.error(message)
            raise SystemExit(message)

        output += row

        if record_num % config['JANRAIN_BATCH_SIZE'] == 0:
            with closing(writerFactory()) as fp:
                fp.write(output)
            output = ""
            logger.debug("wrote record {}".format(record_num))

        record_last_updated = fromRecordDateTime(record['lastUpdated'])
        if not last_updated or record_last_updated > last_updated:
            last_updated = fromRecordDateTime(record['lastUpdated'])
            job.lastupdated = last_updated

    if output:
        with closing(writerFactory()) as fp:
            fp.write(output)
        logger.debug("wrote record {}".format(record_num))

    logger.info("exported {} records".format(record_num))

