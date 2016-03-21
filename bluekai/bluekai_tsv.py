def fromRecords(records, keys=[]):
    return str.join('', fromRecordsIterator(records, keys))

def fromRecordsIterator(records, keys=[]):
    for record in records:
        yield fromRecord(record, keys)

def fromRecord(record, keys=[]):

    uuid = record.get('uuid')

    sub_record = { key: record[key] for key in keys if key in record }

    items = sub_record.items()
    items = filter(lambda pair: pair[0] != "uuid", items)
    items = map(lambda pair: "{}={}".format(pair[0], pair[1]), items)
    items = str.join('|', items)

    row = "{}\t{}\n".format(uuid, items)

    return row
