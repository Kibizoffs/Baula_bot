from datetime import datetime

from config import db

def get_time():
    return datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
