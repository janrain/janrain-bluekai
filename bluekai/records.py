def recordsNewerThan(capture_app, config, date):

    capture_schema = capture_app.get_schema(config['JANRAIN_SCHEMA_NAME'])

    records_iterator = capture_schema.records.iterator(
        filtering="lastUpdated > '{}'".format(date.strftime("%Y-%m-%d %H:%M:%S.%f")),
        batch_size=config['JANRAIN_BATCH_SIZE']
    )

    return records_iterator
