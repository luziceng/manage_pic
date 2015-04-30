__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import  manage_pic_db
from config.const import opt_type
class LogHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        sql="select content, type, created_at, admin from log order by created_at desc "
        res=manage_pic_db.query(sql)
        if res != []:
            for r in res:
                r["type"]=opt_type[r["type"]]
        self.render("log.html",res=res, user=self.user)