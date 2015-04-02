__author__ = 'cheng'
from dbmanager import manage_pic_db
from srvframe.base import LoginBaseHandler
class Dish():
    def insert_into_menu(self, name, introduction, pic, user_id):
        sql="insert into menu (name, introduciton, pic, user_id) values( %s, %s, %s, %s)"

        return manage_pic_db.execute(sql, name, introduction, pic , user_id)

