# Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D
# 데이터 포털 API 크롤링 

import urllib.request
import datetime
import time
import json
import pandas as pd 

ServiceKey = 'Ody77GLuYeR%2FeFqbpduMN2Bi4Cka2fztbgnj6E2Eux1kUhy3e4epR28XKBUaObiqPoVzAizxXMBPXtMyuC9v9Q%3D%3D'


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


def getInterSectionInfo():
    service_url = 'http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'
    params = f'?_type=json&serviceKey={ServiceKey}'  #인증키
    params += f'&pageNo=1'
    params += f'&resultType=json'
    params += f'&CLCT_DT=201809051205'
    url =  service_url +params

    # print(url)
    retData= getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)

def getInterSectionInfo():
    result=[]
    
    jsonData = getInterSectionInfo()

    if jsonData['getCrossCartypeTrafficVolumeList']['header']['code'] == '00' : 
                if jsonData['getCrossCartypeTrafficVolumeList']['items'] =='':
                    print(f'서비스오류')
                else:

                    for item in jsonData['getCrossCartypeTrafficVolumeList']['items']
                        ISTL_LCTN = item['ISTL_LCTN']
                        CLCT_DT = item['CLCT_DT']
                        SUM_LRGTFVL = item['SUM_LRGTFVL']
                        



def main():
    jsonResult = []
    result= []
    natName = ''
    ed=''
    dataEnd=''

    print( ' <<국내 입국한 외국인 통계데이터를 수집합니다>>' )
    nat_cd= input ('국가코드입력(중국:112/ 일본:130 / 필리핀:155)>')
    nStartYear= int(input ('데이터를 몇년부터 수집할까요?'))
    nEndYear= int(input ('데이터를 몇년까지 수집할까요?'))
    ed_cd = 'E' # D: 한국인외래관광객/ E: 방한외국인 

    (jsonResult, result,natName, ed, dataEnd ) =\
        getTourismStatsService(nat_cd, ed_cd, nStartYear,nEndYear)

    if natName == '':
        print('데이터 전달 실패. 공공데이터포털 서비스 확인 요망')
    else:
        #파일저장 csv
        columns = ['입국국가','국가코드','입국연월','입국자수']
        result_df= pd.DataFrame(result,columns=columns)
        result_df.to_csv(f'./{natName}_{ed}_{nStartYear}_{dataEnd}.csv',index=False,
                        encoding='utf-8') # 한글 윈도우에서 열고 싶을 때 cp949, 코딩 빅데이터 할 때 utf-8로 바꿔서 사용
        print('csv파일 저장완료!!')

if __name__ == '__main__':
    main()



