# -*- coding:utf-8 -*-
__author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from model.game import Game
import time
import  os
from config.const import main_material, menu_type
from model.dish import Dish
#from model.menu import Menu
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
        material_id=self.get_argument("material")
        type_id=self.get_argument("type")
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
        content=u"%s上传了%s菜单"%(self.user["username"],name1)
        ids=u"%s-%s"%(user_id, dish_id)
        sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s, %s, %s, now(), 0)"
        manage_pic_db.execute(sql, ids, 2, content, self.user["id"])
        sql="insert into menu_material (menu_id, material_id, user_id) values(%s, %s, %s)"
        manage_pic_db.execute(sql, dish_id, material_id, self.user["id"])
        sql="insert into menu_type (menu_id, type_id, user_id) values(%s, %s, %s)"
        manage_pic_db.execute(sql, dish_id, type_id, user_id)
        self.redirect("/")



class MenuHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        sql="select id,  name , introduction, pic from menu where user_id=%s and status=0 order by created_at asc"
        res=manage_pic_db.query(sql, self.user["id"])

        path="/static/pic/dish/"
        if res is not None:
            for r in res:
                r["pic"]=path + r["pic"]
                sql="select id, game_name from game where id in (select game_id from menu_game  where menu_id=%s and user_id=%s )"
                sql="select game_id from menu_game where menu_id=%s and user_id=%s and status=0"
                tencent=manage_pic_db.query(sql, r["id"], self.user["id"])


                t1=manage_pic_db.query(sql, r["id"], self.user["id"])
                games=[]
                for t in t1:
                    game=manage_pic_db.get("select game_name, id from game where id=%s",t["game_id"])
                    games.append(game)


                r["game"]=games
                sql="select material_id from menu_material where menu_id=%s and user_id=%s"
                t=manage_pic_db.get(sql,r["id"],self.user["id"])
                if t!=None:
                    t=t["material_id"]
                    r["material"]=main_material[t]
                else:
                    r["material"]=None
                sql="select type_id from menu_type where menu_id=%s and user_id=%s"
                t=manage_pic_db.get(sql, r["id"], self.user["id"])
                if t!=None:
                    t=t["type_id"]
                    r["type"]=menu_type[t]
                else:
                    r["type"]=None



        print res
        return self.render("menu.html", res=res, user=self.user)

class DeleteMenuHandler(LoginBaseHandler):
    def get(self, menu_id):
        sql="select id, name from menu where id=%s and user_id=%s and status=0"
        t=manage_pic_db.get(sql, menu_id,self.user["id"])
        if t is None:
            return self.render("404.html")
        #menu_id=self.get_argument("menu_id")
        sql="update menu set status=1 where id=%s"
        print sql
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_bonus set status=1 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="update menu_game set status=1 where menu_id=%s"
        manage_pic_db.execute(sql, menu_id)
        sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s, %s, %s, now(), 0)"
        content=u"%s删除了菜式%s"%(self.user["username"], t["name"])
        ids=u"%s-%s"%(self.user["id"], menu_id)
        manage_pic_db.execute(sql, ids, 6, content, self.user["id"])
        return self.redirect("/menu")


class UpdateMenuHandler(LoginBaseHandler):
    def get(self):
        sql="select id, name, introduction, pic from menu where id=%s and user_id=%s"
        menu_id=self.get_arguments("id",None)
        if menu_id is None:
            return self.redirect("404.html")
        res=manage_pic_db.get(sql, menu_id, self.user["id"])
        if res is None:
            return self.write("404.html")
        res["pic"]="/static/pic/dish/"+res["pic"]
        return self.render("update_menu.html", res=res, user=self.user)
    def post (self):
        id=self.get_argument("id")
        menu_name=self.get_argument("name")
        introduction=self.get_argument("introduction")
        new_pic=self.request.files["new_pic"] or None
        sql="select id  from menu where id=%s and user_id =%s and status=0"
        if manage_pic_db.get(sql, id , self.user["id"]) is None:
            return self.render("404.html")
        if new_pic is None:
            sql="update menu set name=%s and introduction=%s where id=%s"
            manage_pic_db.execute(sql, menu_name, introduction, id)
            content=u"%s更新了菜单%s"%(self.user["username"],menu_name)
            ids=u"%s-%s"%(self.user["id"], id)
            sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s, %s, %s, now(), 0)"
            manage_pic_db.execute(sql, ids, 5,content, self.user["id"])
            return self.redirect("/menu")

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
            content=u"%s更新了菜单%s"%(self.user["username"],menu_name)
            ids=u"%s-%s"%(self.user["id"], id)
            sql="insert into log (ids, type, content, operator_id, created_at, admin) values(%s, %s, %s, %s, now(), 0)"
            manage_pic_db.execute(sql, ids, 5,content, self.user["id"])
            return self.redirect("/menu")
