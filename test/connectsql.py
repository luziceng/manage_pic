__author__ = 'cheng'
from dbmanager import manage_pic_db
ls=manage_pic_db.query("select * from ordinary_user")
for l in ls:
    print l
