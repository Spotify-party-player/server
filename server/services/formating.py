from server.jinjaHelpers import timeToHuman


def format_track_data(room):
    return {
                'tracks': [[i.id, i.name, i.artist.name, timeToHuman(i.duration)] for i in room.tracks],
                'keys': ["id","name", "artist", "duration"],
                'currentlyPlaying': room.currentTrack["item"].id
            }
