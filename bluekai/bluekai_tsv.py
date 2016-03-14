def fromRecords(records):
    return str.join('', fromRecordsIterator(records))

def fromRecordsIterator(records):
    for record in records:
        yield fromRecord(record)

def fromRecord(record):

    uuid = record.get('uuid')

    items = record.items()
    items = filter(lambda pair: pair[0] != "uuid", items)
    items = map(lambda pair: "{}={}".format(pair[0], pair[1]), items)
    items = str.join('|', items)

    row = "{}\t{}\n".format(uuid, items)

    return row
