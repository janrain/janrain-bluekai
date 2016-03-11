from .date_utils import fromRecordDateTime
from .date_utils import toRecordDateTime
from .records import recordsNewerThan

def run(JobModel, writter, config, logger, datalib, converter):

    logger.info("start")

    job = JobModel.get(config)
    err = None

    try:

        do_job(JobModel, writter, config, logger, datalib, converter)

    except Exception as ex:

        err = str(ex)
        logger.exception(ex)

    finally:
        if err:
            job.error = err
            logger.error(err)
        # update db regardless
        job.stop()
        logger.info("end ({} seconds)".format(job.ended - job.started))

def do_job(JobModel, writter, config, logger, datalib, converter):

    job = JobModel.get(config)
    last_updated = job.lastUpdated

    capture_app = datalib.get_app(
        config['JANRAIN_URI'],
        config['JANRAIN_CLIENT_ID'],
        config['JANRAIN_CLIENT_SECRET'])

    records_iterator = recordsNewerThan(capture_app, config, last_updated)

    with writter as fp:

        record_num = 0
        for record_num, record in enumerate(records_iterator, start=1):

            record_last_updated = fromRecordDateTime(record['lastUpdated'])
            if not last_updated or record_last_updated > last_updated:
                last_updated = fromRecordDateTime(record['lastUpdated'])
                job.lastupdated = last_updated

            row = converter(record)

            fp.write(row)

            if record_num % config['JANRAIN_BATCH_SIZE'] == 0:
                logger.debug("wrote record {}".format(record_num))

        logger.info("exported {} records".format(record_num))

    return job
