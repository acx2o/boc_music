import requests, datetime
from bs4 import BeautifulSoup
import sys
import time,json
from flaskr import db, app
from flaskr.models import Artist, Song, Album

def add_artist(artist_name):
    #オブジェクトを新しく作成
    artist = Artist(
        name=artist_name,           #スクレイピングしてきたアーティストの名前を入れる
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    db.session.add(artist)
    # flushしないとidが取れない
    db.session.flush()
    db.session.refresh(artist)
    return artist


def add_song(artist_id, album_id, song_title):
    song = Song(
        title = song_title,          #スクレイピングしてきた曲のタイトル
        artist_id=artist_id,         # 上で作成した Artist の ID （今の場合は 1）
        album_id=album_id,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    db.session.add(song)
    return song

def add_Album(album_title, artist_id, published_at, product_code):
    album = Album(
        title = album_title,        #スクレイピングしたアルバムのタイトルを入れる
        artist_id=artist_id,
        published_at = published_at,    #発売日
        product_code = product_code,    #商品番号
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now()
    )
    db.session.add(album)
    db.session.flush()
    db.session.refresh(album)
    return album


#歌ネットのアルバムがあるアーティストのurlを表示
def main():
    for i in range(45):
        target_url = 'https://www.uta-net.com/name_list/' + str(i)
        # print(target_url)

        r = requests.get(target_url)         #requestsを使って、webから取得
            # print(r.text)

        soup = BeautifulSoup(r.text, 'lxml') #要素を抽出 解析機にいれてる状態をSOUPにした　
                                                    # r.textをHTMLとして扱うためにBeautifulSoupを使う
        artist_list = soup.find('div', id="kana_list")

        if artist_list.select('.album') != None:
            albums = artist_list.select('.album')

        #albumsの中の要素を１つずつ出す
        for album in albums:
            a = album.find("a")#aタグを取り出す
            href = a.attrs['href']
            url = "https://www.uta-net.com" + href
            # print(url)

            clowl_album(url)
            time.sleep(1)           #連続でサーバーにrequestを送ることを防ぐ　
                                    #バンバン送ると怒られるから間を開ける

        db.session.commit()


#urlのなかをさらに掘っていく
def clowl_album(url):
    try:
        album_response = requests.get(url)
        soup = BeautifulSoup(album_response.text, 'lxml')
        # print(soup)
        album_contents = soup.find('div', id="album_contents")
        artist_name = album_contents.select('.artist_name')[0].text
        print(artist_name)


        artist = add_artist(artist_name)    #add_artist関数にartist_nameを入れて実行
        print('Add artist: artistId: {}, name: {}'.format(artist.id, artist.name))
        # print(artist.id)
        # print(artist.name)

        table_items = soup.find_all(attrs={"class": "album_table"})

        for item in table_items:
            album_info = item.find(attrs={"class": "album_title"})
            album_title = album_info.find("p").text
            # print(album_title)
            # if album_info.find_all("dd").length == 2:
            published_at = album_info.find_all("dd")[0].text
            product_code = album_info.find_all("dd")[1].text
            # elif album_info.find_all("dd").length == 1:
            album = add_Album(album_title, artist.id, published_at, product_code)
            # artist, album

            songs = item.find(attrs={"class": "album_songs"}).find_all("li")

            for song in songs:
                song_title = song.text
                add_song( artist.id, album.id, song_title)

                # print(song_title)

    except OSError:
        print("エラーが起きました")
        time.sleep(3)
        clowl_album(url)




if __name__ == '__main__':#scraping.pyを呼びたした時だけ、main()が動くようにしている　これはいつもつけるべき　
    main()
    # ライブラリインポート


    # Slackで通知設定
    URL='https://hooks.slack.com/services/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'
    TEXT='finish!!!!!'
    USERNAME='test_username'

    # post
    post_json = {
        'text': TEXT,
        'username': USERNAME,
        'link_names': 1
    }
    requests.post(URL, data = json.dumps(post_json))



# name = artist_list.select('.name')
# a =

# print(href)
