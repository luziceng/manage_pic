__author__ = 'cheng'
from srvframe.base import LoginBaseHandler
from model.game import Game
class UploadHandler(LoginBaseHandler):
    def get(self, *args, **kwargs):
        games=Game().get_game_id_and_name()
        self.render("upload.html", games)
    def post(self, *args, **kwargs):
        dashs=self.request.file['dash']
        for dash in dashs:
