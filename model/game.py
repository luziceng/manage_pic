__author__ = 'cheng'
from dbmanager import manage_pic_db

class Game():
    def get_game_id_and_name(self):
        sql="select game_name and id from game where status=0"
        return manage_pic_db.query(sql)
