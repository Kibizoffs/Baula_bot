from datetime import datetime

def get_time():
    return datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
