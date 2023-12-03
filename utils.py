from datetime import datetime

def getTime():
    return datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
