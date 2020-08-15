import requests as req
import json
import re
from bs4 import BeautifulSoup

url = [
    "http://bjapi.afreecatv.com/api/killyou18/board?page=pageNum&field=title,contents&keyword=%EB%85%B8%EB%9E%98%EB%A6%AC%EC%8A%A4%ED%8A%B8",
    "http://bjapi.afreecatv.com/api/killyou18/title/title_no?page=1&keyword=%EB%85%B8%EB%9E%98%EB%A6%AC%EC%8A%A4%ED%8A%B8"
]

data = [
    dict(
        Accept= "*/*",
        Origin= "http://bj.afreecatv.com",
        Cookie= ": _ausa=0x8001ea70; _ausb=0x88e6f3df; _ga=GA1.2.1121813587.1597327139; _gid=GA1.2.847855015.1597327139; _gat_gtag_UA_132973034_1=1; __gads=ID=ea151d8cdad22048-223eb569f6c20077:T=1597327153:RT=1597329235:S=ALNI_MaXRCpIRe1mSowzD5Bd1Sqn9RaiCg; _csk=%uB178%uB798%uB9AC%uC2A4%uD2B8; AbroadChk=FAIL; AbroadVod=FAIL; bjStationHistory=%025638745%023061080%021338250%023364971%0213928281%0217577562%022986113; OAX=ffetWV8HX1MABaFO; _au=ce695dcb6adac36d751a7a23a41613c4",
        Host= "bjapi.afreecatv.com",
        Referer= "http://bj.afreecatv.com/killyou18/posts?page=1&keyword=%EB%85%B8%EB%9E%98%EB%A6%AC%EC%8A%A4%ED%8A%B8",
        Connection= "keep-alive",
        allow_redirects=True
    ),
    dict(
        Accept= "*/*",
        Origin= "http://bj.afreecatv.com",
        Cookie= "post_referer=; _ausa=0x14e7aeb0; _ausb=0xdbf5930f; __gads=ID=ea151d8cdad22048-223eb569f6c20077:T=1597327153:RT=1597331770:S=ALNI_MaXRCpIRe1mSowzD5Bd1Sqn9RaiCg; _ga=GA1.2.1121813587.1597327139; _gid=GA1.2.847855015.1597327139; _csk=%uB178%uB798%uB9AC%uC2A4%uD2B8; AbroadChk=FAIL; AbroadVod=FAIL; bjStationHistory=%025638745%023061080%021338250%023364971%0213928281%0217577562%022986113; OAX=ffetWV8HX1MABaFO; _au=ce695dcb6adac36d751a7a23a41613c4",
        Host= "bjapi.afreecatv.com",
        Referer= "http://bj.afreecatv.com/killyou18/post/60126717?page=1&keyword=%EB%85%B8%EB%9E%98%EB%A6%AC%EC%8A%A4%ED%8A%B8",
        Connection= "keep-alive",
        allow_redirects=True
    )
]

r0 = req.get(url[0].replace('pageNum','1'), data[0])
j0 = json.loads(r0.text)
print(j0['meta']['last_page'])


resultFile = open('/Users/jangwonsear/soonMusic.py/soonMusic.json', 'a')
resultFile.write('[')
for page in list(range(1,int(j0['meta']['last_page'])+1)):
    r0 = req.get(url[0].replace('pageNum',str(page)), data[0])
    j0 = json.loads(r0.text)
    print(j0['meta']['current_page'])
    for val in j0['data']:
        r1 = req.get(url[1].replace('title_no',str(val['title_no'])), data[1])
        j1 = json.loads(r1.text)
        '''
        print(
            j1,
            j1['reg_date'],
            j1['title_name'],
            '\n',
            j1['user_id'],
            '\n',
            j1['content']
        )
        '''
        temp = []

        soup = BeautifulSoup(j1['content'])
        # delete between () parenthesis  AND  separate with get_text, get text with semantics (newline especially)
        fullList = re.sub(r" ?\([^)]+\)", "", soup.get_text(separator='|separator|',strip=True)).split('|separator|')
        for item in fullList:
            # if there's '-' or '_'
            if item.find('-') != -1 or item.find('_') != -1:
                # if there's Alphabet
                if re.search('[a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]',item)!=None:
                    # if there is no 'o<-<'
                    if re.search('o<-<',item)==None:
                        # if there is no '-o-'
                        if re.search('-o-',item)==None:
                            resultFile.write(json.dumps({"song":item,"time":j1['reg_date']},ensure_ascii=False)+',')
resultFile.write(']')
resultFile.close()
                    


'''
with open('./soonMusic.py/soonMusic.json','w+',encoding='UTF-8-sig') as outfile:
    json.dump(result, outfile, ensure_ascii=False)
'''

