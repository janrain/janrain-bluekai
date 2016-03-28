def fromRecords(records, keys=[]):
    return str.join('', fromRecordsIterator(records, keys))

def fromRecordsIterator(records, keys=[]):
    for record in records:
        yield fromRecord(record, keys)

def fromRecord(record, keys=None):

    def getKey(key, keys):
        try:
            return keys[key]
        except TypeError:
            return key

    if not keys:
        keys = []

    uuid = record.get('uuid')

    sub_record = { key: record[key] for key in keys if key in record }

    items = sub_record.items()
    items = filter(lambda pair: pair[0] != "uuid", items)
    items = map(lambda pair: "{}={}".format(getKey(pair[0], keys), pair[1]), items)
    items = str.join('|', items)

    row = "{}\t{}\n".format(uuid, items)

    return row
