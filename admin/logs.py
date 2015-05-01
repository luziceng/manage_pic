__author__ = 'cheng'
from srvframe.auth import LoginBaseHandler
from dbmanager import  manage_pic_db
from config.const import opt_type
class LogHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        user_id=self.get_argument("user_id",None)
        opt_type=self.get_argument("opt_type",None)
        res=[]
        if user_id==None and opt_type==0:
            sql="select content, type, created_at, admin from log order by created_at desc "
            res=manage_pic_db.query(sql)
        elif user_id==None and opt_type!=0:
            sql="select content, type, created_at, admin from log where type=%s order by created_at desc"
            res=manage_pic_db.query(sql, opt_type)
        elif user_id !=None and opt_type==0:
            sql="select content, type, created_at ,admin from log where operator_id=%s order by created_at desc"
        elif user_id !=None and opt_type!=0:
            sql="select content, type, created_at , admin from log where operator_id=%s and type=%s order by created_at desc"
        if res != []:
            for r in res:
                r["type"]=opt_type[r["type"]]
        self.render("log.html",res=res, user=self.user)