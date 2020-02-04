import os
import string
import random
from typing import Tuple, Dict
from pprint import pprint
from conf import SECRET_KEY, CLIENT_ID, CLIENT_KEY, REDIRECT_URI
# from server.models import Room


from flask import Flask
from flask_socketio import SocketIO
from server.services import TickTimer
import spotify.sync as spotify


# SPOTIFY_CLIENT = spotify.Client(CLIENT_ID, CLIENT_KEY)

# APP = flask.Flask(__name__)

# APP.config.from_mapping({'spotify_client': SPOTIFY_CLIENT})
# APP.config['SECRET_KEY'] = SECRET_KEY

# OAUTH2_SCOPES: Tuple[str] = ('user-modify-playback-state', 'user-read-currently-playing', 'user-read-playback-state')
# OAUTH2: spotify.OAuth2 = spotify.OAuth2(SPOTIFY_CLIENT.id, REDIRECT_URI, scopes=OAUTH2_SCOPES)

# APP.config['OAUTH2'] = OAUTH2

# SPOTIFY_USERS: Dict[str, spotify.User] = {}



class Player(Flask):
    @staticmethod
    def create_app():
        """
        Application factory
        """

        app = Player(__name__)
        socketio = SocketIO(app)

        return app, socketio

    def setupSpotify(self):
        self.SPOTIFY_CLIENT = spotify.Client(CLIENT_ID, CLIENT_KEY)

        app.config.from_mapping({'spotify_client': self.SPOTIFY_CLIENT})
        app.config['SECRET_KEY'] = SECRET_KEY

        OAUTH2_SCOPES: Tuple[str] = ('user-modify-playback-state', 'user-read-currently-playing', 'user-read-playback-state', 'playlist-modify-public', 'playlist-modify-private')
        self.OAUTH2: spotify.OAuth2 = spotify.OAuth2(self.SPOTIFY_CLIENT.id, REDIRECT_URI, scopes=OAUTH2_SCOPES)

        app.config['OAUTH2'] = self.OAUTH2
        pprint(self.OAUTH2)

        self.SPOTIFY_USERS: Dict[str, spotify.User] = {}
        self.rooms = {}
        self.userToRoom: Dict[str, str] = {}

    def registerBlueprints(self):
        from server.blueprints import webPrint, spotifyPrint
        self.register_blueprint(webPrint)
        self.register_blueprint(spotifyPrint)

    def registerHelpers(self):
        from server.jinjaHelpers import timeToHuman
        self.add_template_filter(timeToHuman)

    def setup(self):
        self.setupSpotify()
        self.registerHelpers()
        self.registerBlueprints()

    def start(self, ip='127.0.0.1', port=8888, debug=True, doSetup=True):
        if doSetup:
            self.setup()
        self.timer = TickTimer()
        socketio.run(self, ip, port=port, debug=debug)
        self.timer.stop()


app, socketio = Player.create_app()

__all__ = [
    'app',
    'socketio',
]