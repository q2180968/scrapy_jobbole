from hashlib import md5


def getHash(data):
    if isinstance(data, str):
        data = data.encode('utf-8')
    m = md5()
    m.update(data)
    return m.hexdigest()
