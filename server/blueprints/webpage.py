from server.blueprints import webPrint
from flask import render_template, request, abort
from server.models import BaseViewModel
from server import app, socketio


@webPrint.route('/')
@webPrint.route('/index')
def index():
    vm = BaseViewModel()
    return render_template('index.html', vm=vm)

@webPrint.route('/room')
def room():
    roomId = request.args.get('tag')
    vm = BaseViewModel(roomId)
    return render_template('room.html', vm=vm)

@webPrint.route('/room/<roomId>/track/<trackId>', methods = ['POST'])
def addTrack(roomId, trackId):
    try:
        room = app.rooms[roomId]
        track = app.SPOTIFY_CLIENT.get_track(trackId)
        room.playlist.add_tracks(track)
        room.update()
        return "OK"
    except KeyError:
        return abort(400)