from logging import Formatter
import sqlite3

env_key_token = 'password_baula_bot'

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
        self.file_path = 'db.sqlite'
        self.con = sqlite3.connect(self.file_path)
        self.cur = self.con.cursor() 
db = DB()

id_key = 'id'
gr_key = 'gr'
last_name_key = 'last_name'
pe_key = 'pe'
baula_key = 'baula'
rubl_key = 'rubl'
sal_key = 'sal'
msg_count_1w_key = 'msg_count_1w'
admin_key = 'admin'
banned_key = 'banned'
thread_stats_key = 'thread_stats'
thread_mathhedgehog = 'thread_mathhedgehog'
thread_profkomvmk = 'thread_profkomvmk'

stats_weekday = 4
stats_hour = 18
stats_minute = 0

baula_rubl_sal_groups = [107, 108]

temp_path = 'Temp'

path_hand = 'Media/Hand/frame{}.png'
path_salnikov = 'Media/salnikov.jpg'
path_trash = 'Media/trash.jpg'
filename_hand = 'hand.gif'
filename_salnikov = 'salnikov.jpg'
filename_trash = 'trash.jpg'
