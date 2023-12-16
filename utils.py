from datetime import datetime
import logging
import os

from config import temp_path

def get_path(s, ext:str) -> str:
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    return f'{temp_path}/{str(s)}.{ext}'

def get_time() -> str:
    return datetime.strptime(str(datetime.utcnow()), '%Y-%m-%d %H:%M:%S.%f')
