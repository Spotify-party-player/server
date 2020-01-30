from conf import PLAYLIST_NAME
from flask import request
from server import app
from server.jinjaHelpers import timeToHuman
from server.services import format_track_data
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect


class Room(object):
    def __init__(self, userId, user, roomId):
        super().__init__()
        self.userId = userId
        self.user = user
        self.roomId = roomId
        self.playlist = None
        for p in user.get_all_playlists():
            if p.name == PLAYLIST_NAME:
                self.playlist = p
                break
        if self.playlist == None:
            self.playlist = self.user.create_playlist(PLAYLIST_NAME)
        self.currentTrack = self.user.currently_playing()
        self.tracks = self.playlist.get_all_tracks()

    def update(self):
        self.currentTrack = self.user.currently_playing()
        self.tracks = self.playlist.get_all_tracks()
        request.namespace = "/sockets"
        with app.app_context():
            emit('update_list', format_track_data(self), room=self.roomId)
