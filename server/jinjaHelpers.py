from datetime import timedelta


def timeToHuman(amount):
    minutes = int(amount/60000)
    seconds = int(amount/1000) - minutes*60
    return f'{minutes}:{seconds:02}'