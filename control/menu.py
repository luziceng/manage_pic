__author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from model.game import Game
import time
import  os
from model.dish import Dish
from model.menu import Menu
from dbmanager import  manage_pic_db
class UploadHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        games=Game().get_game_id_and_name()
        print games
        self.render("upload_menu.html", games=games, user=self.user)

    def post(self, *args, **kwargs):
        introduction=self.get_argument("introduction")
        name1=self.get_argument("name")
        game_id=self.get_arguments("game", None)

        dishes=self.request.files['menu']
        print game_id
        filename=''
        for dish in dishes:
            name=dish['filename']
            firstname=name[:name.rfind(".")]+str(int(time.time()))
            lastname=name[name.rfind('.'):]
            filename=firstname+lastname
            upload_path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            #print upload_path
            upload_path=os.path.join(upload_path,'static')
            #print upload_path
            upload_path=os.path.join(upload_path, 'pic')
            upload_path=os.path.join(upload_path, 'dish')
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:
                up.write(dish['body'])


        user_id=self.user["id"]
        dish_id=Dish().insert_into_menu(name1, introduction, filename, user_id)

        if game_id is not None:
            for id in game_id:
                Game().insert_game_and_dish(id, dish_id,user_id)
        sql="insert into menu_bonus (menu_id, created_at, user_id) values (%s, now(), %s)"
        manage_pic_db.execute(sql, dish_id, user_id)
        self.redirect("/")



class MenuHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        sql="select id,  name , introduction, pic from menu where user_id=%s and status=0 order by created_at asc"
        res=manage_pic_db.query(sql, self.user["id"])
        path="/static/pic/dish/"
        if res is not None:
            for r in res:
                r["pic"]=path + r["pic"]
        return self.render("menu.html", res=res, user=self.user)

class DeleteMenuHandler(LoginBaseHandler):
    def get(self, menu_id):
        #menu_id=self.get_argument("menu_id")
        sql="update menu set status=1 where id=%s"
        print sql
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_bonus set status=1 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_game set status=1 where menu_id=%s"
        return self.redirect("/menu")


class UpdateMenuHandler(LoginBaseHandler):
    def get(self):
        sql="select id, name, introduction, pic from menu where id=%s and user_id=%s"
        menu_id=self.get_arguments("id",None)
        if menu_id is None:
            return self.redirect("/delete")
        res=manage_pic_db.get(sql, menu_id, self.user["id"])
        if res is None:
            return self.write("wrong menu_id")
        res["pic"]="/static/pic/dish/"+res["pic"]
        return self.render("update_menu.html", res=res, user=self.user)
    def post (self):
        id=self.get_argument("id")
        menu_name=self.get_argument("name")
        introduction=self.get_argument("introduction")
        new_pic=self.request.files["new_pic"]
        if new_pic is None:
            sql="update menu set name=%s and introduction=%s where id=%s"
            manage_pic_db.execute(sql, menu_name, introduction, id)
        else:
            filename=''
            for dish in new_pic:
                name=dish['filename']
                firstname=name[:name.rfind(".")]+str(int(time.time()))
                lastname=name[name.rfind('.'):]
                filename=firstname+lastname
                upload_path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
                #print upload_path
                upload_path=os.path.join(upload_path,'static')
                #print upload_path
                upload_path=os.path.join(upload_path, 'pic')
                upload_path=os.path.join(upload_path, 'dish')
                filepath=os.path.join(upload_path,filename)
                with open(filepath,'wb') as up:
                    up.write(dish['body'])
            sql="update menu set name=%s , introduction=%s , pic=%s where id=%s"
            manage_pic_db.execute(sql, menu_name, introduction, filename, id)
            return self.redirect("/menu")