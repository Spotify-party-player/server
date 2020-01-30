from flask import Blueprint


webPrint = Blueprint('web', __name__)
spotifyPrint = Blueprint('spotify', __name__)


from server.blueprints.webpage import index, room, addTrack
from server.blueprints.spotify import spotify_callback, spotify_failed, signIn, getTracks
from server.blueprints.sockets import join_room, connect