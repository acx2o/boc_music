from flaskr import db
from datetime import datetime

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    songs = db.relationship('Song', backref='artist', lazy=True)
    albums = db.relationship('Album', backref='artist', lazy=True)
    # songname = db.Column(db.Text)
    # artist = db.Column(db.Text)

class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer,  db.ForeignKey('artists.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    created_at = db.Column(db.DateTime, nullable=False)
    published_at = db.Column(db.Integer, nullable=False)
    product_code = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    songs = db.relationship('Song', backref='albums', lazy=True)


# これを書くと、このかかれたものは、カラムを持っていることを示してくれる
def __repr__(self):
    return '<Artist id={id} name={artist_name!r}>'.format(
                id=self.id, name=self.name)

def init():
    print("==============================")
    db.create_all()
