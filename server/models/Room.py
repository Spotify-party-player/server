from conf import PLAYLIST_NAME
from flask import request
from server import app, socketio
from server.jinjaHelpers import timeToHuman
from server.services import format_track_data
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect
from threading import Lock


class Room(object):
    def __init__(self, userId, user, roomId):
        super().__init__()
        self.userId = userId
        self.user = user
        self.player = self.user.get_player()
        self.roomId = roomId
        self.playlist = None
        for p in user.get_all_playlists():
            if p.name == PLAYLIST_NAME:
                self.playlist = p
                break
        if self.playlist == None:
            self.playlist = self.user.create_playlist(PLAYLIST_NAME)
        self.currentTrack = self.user.currently_playing()
        self.lastTrack = self.currentTrack
        self.tracks = self.playlist.get_all_tracks()
        self.connected = 1
        self.skip = []
        self.next = {}
        thread_lock = Lock()
        self.threadShouldRun = True
        with app.app_context():
            with thread_lock:
                self.thread = socketio.start_background_task(self.background_task)

    def background_task(self):
        while self.threadShouldRun:
            socketio.sleep(10)
            self.update_current()

    def close_room(self):
        self.threadShouldRun = False

    def update_list(self):
        with app.app_context():
            emit('update_list', format_track_data(self), room=self.roomId, namespace = "/sockets")

    def update_current(self):
        self.currentTrack = self.user.currently_playing()
        if self.currentTrack == {}:
            return
        if self.currentTrack["item"].id != self.lastTrack["item"].id:
            self.skip = []
            self.update_list()
            self.update_active()

    def update(self):
        self.tracks = self.playlist.get_all_tracks()
        self.update_list()

    def update_active(self):
        self.connected = 0
        with app.app_context():
            emit('get_active', format_track_data(self), room=self.roomId, namespace = "/sockets")

    def skip_current(self, sid):
        if sid not in self.skip:
            self.skip.append(sid)
        else:
            return

        if len(self.skip) > 0 and len(self.skip) > self.connected/2:
            self.player.next()
            self.update_current()
        else:
            self.update_list()
