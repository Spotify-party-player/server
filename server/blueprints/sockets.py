from server import socketio, app
from server.services import format_track_data
from threading import Lock
from flask_socketio import emit, join_room, leave_room, \
    close_room, rooms, disconnect

@socketio.on('connect', namespace='/sockets')
def connect():
    emit('connected', {'data': 'Connected', 'count': 0})

@socketio.on('join', namespace='/sockets')
def join(msg):
    print(msg)
    room = msg["roomId"]
    join_room(room)
    emit('update_list', format_track_data(app.rooms[room]), room=room)