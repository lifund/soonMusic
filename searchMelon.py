from bs4 import BeautifulSoup
import json
import urllib
import requests as req

# http://pycurl.io/docs/latest/quickstart.html#following-redirects
import pycurl
import certifi
from io import BytesIO

import os
soonMusic = open('/Users/jangwonsear/soonMusic.py/soonMusic.json', 'r')
j = json.load(soonMusic)



def searchGenie(searchString):
    return searchString

def searchMelon(searchString):
    searchURL = "https://www.melon.com/search/total/index.htm?q=searchString&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&linkOrText=T&ipath=srch_form".replace("searchString", urllib.parse.quote(searchString))
    print(searchURL)
    buffer1 = BytesIO()
    c1 = pycurl.Curl()
    c1.setopt(pycurl.URL, searchURL)
    c1.setopt(pycurl.WRITEDATA, buffer1)
    c1.setopt(pycurl.CAINFO, certifi.where())
    c1.perform()
    c1.close()
    buf1 = buffer1.getvalue()
    body1 = buf1.decode('utf-8')
    if len(body1.split("goSongDetail('")) == 1:
        print('No melon search result :', searchString)
        print('... searching other platforms ...')
    else:
        songCode = body1.split("goSongDetail('")[1].split("')")[0]

        searchURL2 = "https://www.melon.com/song/detail.htm?songId=songCode".replace("songCode", songCode)
        buffer2 = BytesIO()
        c2 = pycurl.Curl()
        c2.setopt(pycurl.URL, searchURL2)
        c2.setopt(pycurl.WRITEDATA, buffer2)
        c2.setopt(pycurl.CAINFO, certifi.where())
        c2.perform()
        c2.close()
        buf2 = buffer2.getvalue()
        body2 = buf2.decode('utf-8')
        artistCode = body2.split("goArtistDetail('")[1].split("')")[0]
        soup2 = BeautifulSoup(body2,'html.parser')

        searchURL3 = "https://www.melon.com/artist/timeline.htm?artistId=artistCode".replace("artistCode", artistCode)
        buffer3 = BytesIO()
        c3 = pycurl.Curl()
        c3.setopt(pycurl.URL, searchURL3)
        c3.setopt(pycurl.WRITEDATA, buffer3)
        c3.setopt(pycurl.CAINFO, certifi.where())
        c3.perform()
        c3.close()
        buf3 = buffer3.getvalue()
        body3 = buf3.decode('utf-8')
        soup3 = BeautifulSoup(body3,'html.parser')
        

        
        result = json.dumps({
            "melon" : {
                "songCode" : songCode,
                "song_name" : soup2.select('#downloadfrm > div > div > div.entry > div.info > div.song_name')[0].text.replace('곡명','').strip(),
                "artistCode" : artistCode,
                "artist_name" : soup2.select('#downloadfrm > div > div > div.entry > div.info > div.artist')[0].text.replace('\n',''),
                "artist_image" : soup3.select('#artistImgArea > img')[0]['src'],
                "genre" : [g.strip() for g in soup2.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)')[0].text.split(',')],
                "release_date" : soup2.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)')[0].text,
                "album_name" : soup2.select('#downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a')[0].text
            },
            "genie" : {
                "songCode" : "",
                "song_name" : "",
                "artistCode" : "",
                "artist_name" : "",
                "artist_image" : "",
                "genre" : "",
                "release_date" : "",
                "album_name" : ""
            },
            "youtube" : {
                "videoCode" : "",
                "video_name" : "",
                "video_thumb" : "",
                "is_music" : "",
                "songCode" : "",
                "song_name" : "",
                "artistCode" : "",
                "artist_name" : "",
                "artist_image" : "",
                "genre" : "",
                "release_date" : "",
                "album_name" : ""
            }
        },ensure_ascii=False,indent=2)
        return result

for i in range(0,10):
    print(searchMelon(j[i]['song']))

# goSongDetail('~')
# https://www.melon.com/song/detail.htm?songId=~
    # 곡 이름
    # #downloadfrm > div > div > div.entry > div.info > div.song_name
    # 아티스트 이름
    # #downloadfrm > div > div > div.entry > div.info > div.artist
    # 장르
    # #downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(6)
    # 발매일
    # #downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(4)
    # 앨범
    # #downloadfrm > div > div > div.entry > div.meta > dl > dd:nth-child(2) > a

# goArtistDetail('~')
# https://www.melon.com/artist/timeline.htm?artistId=~
    # 아티스트 이미지
    # #artistImgArea > img