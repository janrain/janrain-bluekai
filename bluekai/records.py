from datetime import datetime
from .date_utils import toRecordDateTime

def recordsNewerThan(capture_app, config, date=None):

    capture_schema = capture_app.get_schema(config['JANRAIN_SCHEMA_NAME'])

    attributes = set(config['JANRAIN_ATTRIBUTE_KEYS']) | set(('uuid', 'lastUpdated'))

    if not date:
      date = datetime.utcfromtimestamp(0)

    records_iterator = capture_schema.records.iterator(
        filtering="lastUpdated > '{}'".format(toRecordDateTime(date)),
        batch_size=config['JANRAIN_BATCH_SIZE'],
        attributes=sorted(attributes)
    )

    return records_iterator
