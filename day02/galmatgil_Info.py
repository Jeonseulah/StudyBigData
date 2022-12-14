#부산 갈맷길 정보 API 크롤링 
from operator import itemgetter
import os
import sys
import urllib.request
import datetime
import time
import json
import pandas as pd 
import pymysql

ServiceKey = 'hxyib50euy22Wz9%2Bn7G5JYgT9pz8woNjRsRbmiNBZGrCNVdYBYeq7DCCZnGVHGXxBFCjxsHfU7gVPRX%2B8WPYKA%3D%3D'

# url 접속 요청 후 응답리턴 함수 
def getRequestUrl(url):
    
    # URL 접속 요청 후 응답함수
    # -------------------------
    # parameter : url -> openAPI 전체 URL

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


def getGalmatgilInfo():
    service_url = 'http://apis.data.go.kr/6260000/fbusangmgcourseinfo/getgmgcourseinfo'
    params = f'?serviceKey={ServiceKey}'
    params += '&numOfRows=10'
    params += '&pageNo=1'
    params += '&resultType=json'
    url = service_url + params

    retData = getRequestUrl(url)

    if retData == None:
        return None
    else:
        return json.loads(retData)

def getGalmatgilService():
    result = []

    jsonData = getGalmatgilInfo()
    # print(jsonData)
    if jsonData['getgmgcourseinfo']['header']['code'] =='00':
        if jsonData['getgmgcourseinfo']['item']=='':
            print('서비스오류!!!')
        else:
            for item in jsonData['getgmgcourseinfo']['item']:
                seq = item['seq']
                course_nm = item['course_nm']
                gugan_nm = item['gugan_nm']
                gm_range =item['gm_range']
                gm_degree =item['gm_degree']
                start_pls =item['start_pls']
                start_addr =item['start_addr']
                middle_pls =item['middle_pls']
                middle_adr =item['middle_adr']
                end_pls =item['end_pls']
                end_addr =item['end_addr']
                gm_course =item['gm_course']
                gm_text =item['gm_text']

                result.append([seq, course_nm, gugan_nm, gm_range, gm_degree, start_pls, start_addr, middle_pls, middle_adr, end_pls, end_addr, gm_course,gm_text])
    return  result

def main():
    result = []

    print('부산 갈맷길 코스 조회합니다')
    result = getGalmatgilService()

    if len(result) > 0:
        #csv파일저장
        columns = ['seq','course_nm','gugan_nm','gm_range','gm_degree','start_pls','start_addr', 'middle_pls','middle_adr','end_pls','end_addr', 'gm_course','gm_text']
        result_df= pd.DataFrame(result,columns=columns)
        result_df.to_csv(f'./부산갈맷길정보.csv',index=False,encoding='utf-8')
        
        print('csv파일 저장완료!!')


# DB 저장

        connection = pymysql.connect(host='localhost', user= 'root', password='1234', db= 'crawling_data')
        cursor = connection.cursor()

        #컬럼명 동적으로 만들기 
        cols= ','.join([str(i) for i in result_df.columns.tolist()])

        for i, row in result_df.iterrows():
            sql= 'INSERT INTO galmatgil_info ('+cols+') VALUES ('+'%s,'*(len(row)-1)+'%s)'
            cursor.execute(sql, tuple(row))

        connection. commit()
        
        print('DB 저장완료')
        connection. close()

if __name__== '__main__':
    main()
