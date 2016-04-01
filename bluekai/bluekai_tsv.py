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

    def getValue(value):
        if isinstance(value, (dict, list)):
            raise TypeError("Plural, Object and JSON value types are not supported")
        elif value is None:
            return ""
        else:
            return value

    if not keys:
        keys = []

    uuid = record.get('uuid')

    sub_record = { key: record[key] for key in keys if key in record }

    items = sub_record.items()
    items = filter(lambda pair: pair[0] != "uuid", items)
    items = map(lambda pair: "{}={}".format(getKey(pair[0], keys), getValue(pair[1])), items)
    items = str.join('|', items)

    row = "{}\t{}\n".format(uuid, items)

    return row
