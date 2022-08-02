from asyncio import ensure_future
import os
from re import I
import sys
from textwrap import indent
import urllib.request
import urllib.parse
import datetime
import time
import json

Client_id='Sk_0fSIdSLCo8Gu5xk_v'
Client_secret='5sqgEFINPE'

# url 접속 요청 후 응답리턴 함수 
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header('X-Naver-Client-Id',Client_id)
    req.add_header('X-Naver-Client-Secret',Client_secret)
    
    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: # 200 OK,400 error, 500 server error
            print(f'[{datetime.datetime.now()}] url Request success')
            return res.read().decode('utf-8')
    except Exception as e: 
        print(e)
        print(f'[{datetime.datetime.now()}]Error for URL:{url}')
        return None
        
def getNaverSearch(node, srcText, start, display):
    base = 'https://openapi.naver.com/v1/search'
    node = f'/{node}.json'
    Text = urllib.parse.quote(srcText) #url주소에 맞춰서 파싱 
    params = f'?query={Text}&start={start}&display={display}'

    url = base + node + params
    resDecode = getRequestUrl(url)
    if resDecode == None:
        return None
    else:
        return json.loads(resDecode)

def  getPostData(post, jsonResult, cnt):
     title = post['title']
     description = post['description']
     originallink = post['originallink']
     link = post['link']
     pubDate = datetime.datetime.strptime(post['pubDate'],'%a, %d %b %Y %H:%M:%S +0900')
     pubDate = pubDate.strftime( '%Y %m %d %H:%M:%S +0900')# 2022-08-02 15:56:34

     jsonResult.append({'cnt':cnt,'title':title,'description':description,'originallink':originallink,'link':link,'pubDate':pubDate})

# 실행최초함수 
def main():
    node = 'news'#크롤링할 대상 
    srcText = input('검색어를 입력하세요:')
    cnt=0
    jsonResult = []
    jsonRes = getNaverSearch(node, srcText, 1, 50)

    #print(jsonRes)
    total = jsonRes['total'] # 검색된 뉴스 개수 

    while ((jsonRes  !=None)and(jsonRes['display']  !=0)):
        for post in jsonRes['items']:
            cnt+=1
            getPostData(post,jsonResult,cnt)
        start = jsonRes['start'] + jsonRes['display'] # 1+50 
        jsonRes = getNaverSearch(node, srcText, start, 50)
    print(f'전체검색:{total} 건')

#file output
    with open(f'./{srcText}_naver_{node}.json', mode='w', encoding='utf-8') as outfile:
        jsonFile = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(jsonFile)

    print(f'가져온 데이터 :{cnt}건')
    print(f'{srcText}_naver_{node},json SAVED')

if __name__ == '__main__':
    main()





