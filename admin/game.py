__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
import  os
import time
from dbmanager import manage_pic_db
import json
import tornado.web
class GameHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("game.html")
    def post(self, *args, **kwargs):
        game_name=self.get_argument("game_name")
        introduction=self.get_argument("introduction")
        print self.request.files
        pic=self.request.files["pic"]
        upload_path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
        upload_path=os.path.join(upload_path,'static')
        upload_path=os.path.join(upload_path, 'pic')
        upload_path=os.path.join(upload_path,'game')
        filename=''
        for meta in pic:
            filename=meta['filename']
            firstname=filename[:filename.rfind('.')]+str(int(time.time()))
            lastname=filename[filename.rfind('.'):]
            filename=firstname+lastname
            filepath=os.path.join(upload_path, filename)
            with open(filepath,'wb') as up:
                up.write(meta['body'])
        sql="insert into game (game_name, introduction, pic, status, created_at) values(%s, %s, %s, 0, now())"
        game_id=manage_pic_db.execute(sql, game_name, introduction, filename)
        res=json.dumps({"game_id":game_id})
        self.write(res)
class GameMenuHandler(tornado.web.RequestHandler):
    def get(self, game_id):
        sql = "select menu_id from menu_game where game_id=%s"
        res=manage_pic_db.query(sql, game_id)
        for r in res:
            sql="select name , pic, introduction from menu where id=%s"
            t=manage_pic_db.get(sql, r["menu_id"])
            r["name"]=t["name"]
            r["pic"]=t["pic"]
            r["introduction"]=r["introduction"]
            sql="select bonus from menu_bonus where menu_id=%s"
            s=manage_pic_db.get(sql, r["menu_id"])
            r["bonus"]=s["bonus"]
        res=json.dumps(res)
        self.write(res)