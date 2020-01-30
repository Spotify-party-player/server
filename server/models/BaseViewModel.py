from server import app


class BaseViewModel(object):
    def __init__(self, roomId = None):
        super().__init__()
        self.roomId = roomId
        self.room = None
        if roomId:
            self.room = app.rooms[roomId]