__author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from model.game import Game
import time
import  os
from model.dish import Dish
class UploadHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        games=Game().get_game_id_and_name()
        self.render("upload.html", games)
    def post(self, *args, **kwargs):
        dashes=self.request.file['dish']
        filename=''
        for dash in dashes:
            name=dash['filename']
            firstname=name[:name.rfind(".")]+str(int(time.time()))
            lastname=name[name.rfind('.'):]
            filename=firstname+lastname
            upload_path=os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            #print upload_path
            upload_path=os.path.join(upload_path,'static')
            #print upload_path
            upload_path=os.path.join(upload_path, 'pic')
            upload_path=os.path.join(upload_path, 'dash')
            filepath=os.path.join(upload_path,filename)
            with open(filepath,'wb') as up:
                up.write(dash['body'])

        introduction=self.get_argument("introduction")
        name=self.get_argument("name")
        game_id=self.request.get("game_id")
        user_id=self.user["id"]
        dish_id=Dish().insert_into_menu(name, introduction, filename, user_id)
        for id in game_id:
            Game().insert_game_and_dish(id, dish_id)
        self.redirect("/")




