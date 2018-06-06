from flaskr.twitter2 import tweet_collect
from flaskr.youtube2 import youtube_search
from flask import request, redirect, url_for, render_template, flash, jsonify
from flaskr import db, app
from flaskr.models import Artist, Song, Album
from sqlalchemy.dialects import mysql

#最初の検索画面
@app.route('/', methods=['GET'])
def search_artist():
    artists = Artist.query.all()
    return render_template('search_artist.html', artists=artists)

@app.route('/artists', methods=['GET'])
def artists():
    keyword = request.args.get('keyword')
    # print(keyword)
    likekeyword = "%" + keyword + "%"
    print(likekeyword)
    artists = Artist.query.filter(Artist.name.like(likekeyword)).all()
    query = Artist.query.filter(Artist.name.like(likekeyword))
    print(query.statement.compile(dialect=mysql.dialect(),
                                  compile_kwargs={"literal_binds": True}))
    print(artists)
    return render_template('search_artist_select.html', artists=artists)

@app.route('/show_artist/<int:artist_id>', methods=['GET'])
def show_artist(artist_id):
    artist = Artist.query.get(artist_id)
    # songs = Song.query.all()
    songs = artist.songs
    albums = artist.albums
    print("-------------------")
    print(songs)
    print("aaaaaaaaaaaaaaaaaaa")
    print(albums)

    for album in albums:
        print(album.songs)
    # return jsonify(songs[0])
    return render_template('show_artist.html', artist=artist, albums=albums, songs=songs)

@app.route('/show_video/<int:song_id>', methods=['GET'])
def show_video(song_id):
    song = Song.query.get(song_id)
    video_id = youtube_search(query=song.title+' '+song.artist.name)
    return render_template('show_video.html', video_id=video_id, song=song)

@app.route('/tweet', methods=['GET'])
def show_tweet():
    return render_template('twitter.html')

@app.route('/tweet', methods=['POST'])
def search_tweet():
    keyword = request.form['keyword']   #フォームから入力された値をKeywordという変数に代入
    print(keyword)
    response = tweet_collect(keyword)   #関数を起動させてTwitterの情報を取得
    return render_template('show_tweets.html',res_text=response)
    # jsonify(response)
