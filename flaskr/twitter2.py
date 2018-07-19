from requests_oauthlib import OAuth1Session
import sys
import json
import datetime, time
import os

def tweet_collect(keyword):

    CK = os.environ['CK']      # Consumer Key
    CS = os.environ['CS']      # Consumer Secret
    AT = os.environ['AT']      # Access Token
    AS = os.environ['AS']      # Accesss Token Secert

    session = OAuth1Session(CK, CS, AT, AS)

    url = 'https://api.twitter.com/1.1/search/tweets.json'
    name = keyword  #argvは配列だから配列型に指定してあげないといけない
    print(name[1])
    res = session.get(url, params = {'q':name, 'count':20})

    #--------------------
    # ステータスコード確認
    #--------------------
    if res.status_code != 200:
        print ("Twitter API Error: %d" % res.status_code)
        sys.exit(1)

    #--------------
    # ヘッダー部
    #--------------
    print ('アクセス可能回数 %s' % res.headers['X-Rate-Limit-Remaining'])
    print ('リセット時間 %s' % res.headers['X-Rate-Limit-Reset'])
    sec = int(res.headers['X-Rate-Limit-Reset'])\
               - time.mktime(datetime.datetime.now().timetuple())
    print ('リセット時間 （残り秒数に換算） %s' % sec)

    #--------------
    # テキスト部
    #--------------
    res_text = json.loads(res.text)
    for tweet in res_text['statuses']:
        print ('-----')
        print (tweet['created_at'])
        print (tweet['text'])

    return res_text
