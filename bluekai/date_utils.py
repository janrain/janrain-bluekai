from datetime import datetime

epoch = datetime.utcfromtimestamp(0)

def fromRecordDateTime(record_field):
    return datetime.strptime(record_field.replace(' +0000', '').split('.')[0], '%Y-%m-%d %H:%M:%S')

def toRecordDateTime(datetime_object):
    return datetime_object.strftime("%Y-%m-%d %H:%M:%S")

def fromModelDateTime(model_datetime=0):
    return datetime.utcfromtimestamp(model_datetime)

def toModelDateTime(datetime_object):
    return (datetime_object - epoch).total_seconds()
