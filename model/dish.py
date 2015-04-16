__author__ = 'cheng'
from dbmanager import manage_pic_db
from srvframe.base import LoginBaseHandler
class Dish():
    def insert_into_menu(self, name, introduction, pic, user_id):
        sql="insert into menu (name, introduction, pic, user_id, created_at) values( %s, %s, %s, %s, now())"

        return manage_pic_db.execute(sql, name, introduction, pic , user_id)

