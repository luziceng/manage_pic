__author__ = 'cheng'
from dbmanager import manage_pic_db

class Game():
    def get_game_id_and_name(self):
        sql="select id , game_name from game where status=0"
        return manage_pic_db.query(sql)


    def insert_game_and_dish(self, game_id, menu_id):
        sql="insert into menu_game (game_id, menu_id)  values(%s, %s)"
        return manage_pic_db.execute(sql,game_id, menu_id )