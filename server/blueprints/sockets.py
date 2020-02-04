from server import socketio, app
from server.services import format_track_data
from threading import Lock
from flask import request
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect

@socketio.on('connect', namespace='/sockets')
def connect():
    emit('connected', {'data': 'Connected', 'count': 0})

@socketio.on('join', namespace='/sockets')
def join(msg):
    try:
        roomId = msg["roomId"]
        join_room(roomId)
        emit('update_list', format_track_data(app.rooms[roomId]), room=roomId)
        app.rooms[roomId].update_active()
    except KeyError:
        pass
    except NameError:
        pass

@socketio.on('active', namespace='/sockets')
def active(msg):
    try:
        roomId = msg["roomId"]
        app.rooms[roomId].connected += 1
    except KeyError:
        pass
    except NameError:
        pass

@socketio.on('skip', namespace='/sockets')
def skip(msg):
    try:
        roomId = msg["roomId"]
        app.rooms[roomId].skip_current(request.sid)
    except KeyError:
        pass
    except NameError:
        pass
