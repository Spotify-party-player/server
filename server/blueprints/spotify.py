from server.blueprints import spotifyPrint
from conf import REDIRECT_URI
from server import app
from server.models import Room
import spotify.sync as spotify
import flask
import os
import string
import random


@spotifyPrint.route('/spotify/callback')
def spotify_callback():
    try:
        code = flask.request.args['code']
    except KeyError:
        return flask.redirect('/spotify/failed')
    else:
        key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
        print(key)
        app.SPOTIFY_USERS[key] = spotify.User.from_code(
            app.SPOTIFY_CLIENT,
            code,
            redirect_uri=REDIRECT_URI#,
            # refresh=True
        )

        flask.session['spotify_user_id'] = key
        roomId = ''.join(random.choice(string.ascii_uppercase) for _ in range(8))
        app.rooms[roomId] = Room(key, app.SPOTIFY_USERS[key], roomId)
        app.userToRoom[key] = roomId

    return flask.redirect(f'/room?tag={app.rooms[app.userToRoom[key]].roomId}')

@spotifyPrint.route('/spotify/failed')
def spotify_failed():
    flask.session.pop('spotify_user_id', None)
    return 'Failed to authenticate with Spotify.'

@spotifyPrint.route('/signin')
def signIn():
    try:
        key = flask.session['spotify_user_id']
        return flask.redirect(f'/room?tag={app.rooms[app.userToRoom[key]].roomId}')

    except KeyError:
        return flask.redirect(app.OAUTH2.url)

@spotifyPrint.route('/tracks/<name>')
def getTracks(name):
    if name == "":
        return flask.abort(400)
    tracks = app.SPOTIFY_CLIENT.search(name, types=["track"])
    return flask.jsonify(
        tracks = [[i.id, i.name, i.artist.name] for i in tracks.tracks],
        keys = ["id","name", "artist"]
    )
