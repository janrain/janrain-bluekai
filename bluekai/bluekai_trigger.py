from hashlib import md5

def fromData(filename, data):
    data_size = len(data)
    data_md5sum = md5(data).hexdigest()
    return "FILE={}\nSIZE={}\nMD5SUM={}".format(filename, data_size, data_md5sum)
