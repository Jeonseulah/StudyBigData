## Selenium 사용 웹페이지 크롤링 (selenium + BeautifulSoup 버전)
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time


def getCoffeeBeanStoreInfo(result):
    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"
    wd = webdriver.Chrome('C:/Users/admin/Desktop/chromedriver.exe') # chrome webdriver 객체 생성
                                                                     # 만약 day03 폴더에 넣었다면 ./day03/chromedriver.exe로 불러온다.
    
    for i in range(1, 5): # 가장 최근 생긴 카페의 매장번호는 381이기 때문에 382까지 써줘야 한다. test할 때에는 작은 숫자로 테스트하자.
        wd.get('https://www.coffeebeankorea.com/store/store.asp') # 왜 여기서 wd를 새로 여는 걸까? 아 아까처럼 열린 상태에서 하면 안 되니까~~
        time.sleep(0.1) # 화면이 로딩될 시간도 필요하다.
        try :
            wd.execute_script(f'storePop2({i})')
            time.sleep(0.1) #팝업이 뜰 시간을 확보하기 위해서 기다리기 위해 time을 쓴다.
            html = wd.page_source
            soup = BeautifulSoup(html, 'html.parser')
            store_id = i # 이건 내가 추가한 부분인데 이것을 id로 사용하고 index=True 대신 index=False로 작업했다.
            store_name = soup.select_one('div.store_txt > h2').string
            print(f'{store_id} : {store_name}')
            store_info = soup.select('div.store_txt > table.store_table > tbody > tr > td')
            store_address_list = list(store_info[2])
            store_address = store_address_list[0].strip()
            store_contact = store_info[3].string
            result.append([store_id, store_name, store_address, store_contact])
            # result.append([store_name]+[store_address]+[store_phone]) 교재 예시는 이거지만 원래 쓰던 방식인 위와 동일함.
        except Exception as e:
            print(e)
            continue
    return


def main():
    result = []
    print('CoffeeBean store Crawling >>>')
    getCoffeeBeanStoreInfo(result)
    
    columns = ['store_id', 'store_name', 'address', 'contact']
    CoffeeBean_df = pd.DataFrame(result, columns=columns)
    CoffeeBean_df.to_csv('./CoffeeBean.csv', encoding='utf8', index=False)
    
    print('저장 완료')
    
if __name__ =='__main__':
    main()