# Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D
# 데이터 포털 API 크롤링 

import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd 

ServiceKey : 'Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D'


# url 접속 요청 후 응답리턴 함수 # 한줄삭제(shift+delete) # (ctrl+space bar)
def getRequestUrl(url):
    req = urllib.request.Request(url)
    
    try:
        res = urllib.request.urlopen(req)
        if res.getcode() == 200: # 200 OK,400 error, 500 server error
            print(f'[{datetime.datetime.now()}] url Request success')
            return res.read().decode('utf-8')
    except Exception as e: 
        print(e)
        print(f'[{datetime.datetime.now()}]Error for URL:{url}')
        return None

#202201, 110, D
def getTourismStatsItem(yyyymm,nat_cd,ed_cd):
    service_url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    params = f'?_type = json&serviceKey={ServiceKey}'  #인증키
    params += f'&YM={yyyymm}'
    params += f'&nat_cd={nat_cd}'
    params += f'&ed_cd={ed_cd}'
    url =  service_url +params

    print(url)

def main():
    print( ' >>국내 입국한 외국인 통계데이터를 수집합니다>>' )
    nat_cd: input ('국가코드입력(중국:112/ 일본:130 / 필리핀:155)>')
    nStartYear: int(input ('데이터를 몇년부터 수집할까요?'))
    nEndYear: int(input ('데이터를 몇년까지 수집할까요?'))
    ed_cd = 'E' # D: 한국인외래고나광객/ E: 방한외국인 

    getTourismStatsItem( nEndYear,nat_cd,ed_cd)

if __name__ == '__main__':
    main()



