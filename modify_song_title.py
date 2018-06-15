import re
from flaskr import db
from flaskr.models import Artist, Song, Album

songs = Song.query.all()
for song in songs:
    #正規表現を使うときは 're' が必要
    #'^'ハットという。先頭の文字を表している
    #'\d+'が何桁でも数字を表している
    #'\d'が１桁の数字を表している
    #^[\d+] が  ''にreplaceされた
    song_name = re.sub(r'^[\d]+', '', song.title)
    song_name = song_name.replace('\n', '')
    song.title = song_name
    print(song.title)
    db.session.add(song)
    db.session.commit()
