from .date_utils import fromRecordDateTime
from .date_utils import toRecordDateTime
from .date_utils import fromModelDateTime
from .date_utils import toModelDateTime

def run(JobModel, writter, config, logger, records_iterator, converter):

    job = JobModel.get(config)
    last_updated = job.lastUpdated

    logger.info("start")

    with writter as fp:

        record_num = 0
        for record_num, record in enumerate(records_iterator, start=1):

            record_last_updated = fromRecordDateTime(record['lastUpdated'])
            if record_last_updated > last_updated:
                last_updated = fromRecordDateTime(record['lastUpdated'])
                job.lastupdated = toModelDateTime(last_updated)

            row = converter(record)

            # write to remote file
            fp.write(row)

            if record_num % config['JANRAIN_BATCH_SIZE'] == 0:
                logger.debug("wrote record {}".format(record_num))

        logger.info("exported {} records".format(record_num))


