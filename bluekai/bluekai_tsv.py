def fromRecords(records):
    return str.join('', fromRecordsIterator(records))

def fromRecordsIterator(records):
    for record in records:
        yield fromRecord(record)

def fromRecord(record):

    uuid = record.get('uuid')

    items = record.iteritems()
    items = filter(lambda (key, value): key != "uuid", items)
    items = map(lambda (key, value): "{}={}".format(key, value), items)
    items = str.join('|', items)

    row = "{}\t{}\n".format(uuid, items)

    return row
