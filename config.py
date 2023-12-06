from logging import Formatter
import sqlite3

env_key_token = 'password_baula_bot'

admin_ids = [280099956]

class Log:
    def __init__(self):
        self.backup_count = 1
        self.file_path = 'baula.log'
        self.file_format = Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s', '%Y-%m-%d %H:%M:%S')
        self.stream_format = Formatter('%(message)s')
        self.max_size = 2 * 1024 * 1024  # 2Mb
log = Log()

class DB:
    def __init__(self):
        self.max_size = 2560
        self.file_path = 'db.sqlite'
        self.con = sqlite3.connect(self.file_path)
        self.cur = self.con.cursor()
        
db = DB()