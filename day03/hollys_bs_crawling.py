from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

# 먼저 jupyter-notebook로 테스트 해본다. 
# (File -> New File... -> jupyter notebook 파일 선택)

def getHollysStoreInfo(result): # 테스트 했던 것을 py파일로 옮기면서 함수로 만들어준다(def). 
    
    for page in range(1, 2):  
		# 테스트할 때는 54(총 53페이지임) 대신 2(1페이지만) 쓰고 실행시켜본다.

        Hollys_url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={page}&sido=&gugun=&store=' 
				# 페이지를 1~53페이지까지 돌아가면서 넣게 된다.

        html = urllib.request.urlopen(Hollys_url)
        soup = BeautifulSoup(html, 'html.parser')
        tag_tbody = soup.find('tbody')

        for store in tag_tbody.find_all('tr'):
            if len(store) <= 3:
                break

            store_td = store.find_all('td')

            store_name = store_td[1].string
            store_sido = store_td[0].string
            store_address = store_td[3].string
            store_phone = store_td[5].string

            result.append([store_name]+[store_sido]+[store_address]+[store_phone])

    print('완료')

def main():
    result = []
    print('할리스 매장 크롤링>>>') 
    getHollysStoreInfo(result)
    
    # 판다스가 제공하는 기능인 데이터프레임 생성
    hollys_df = pd.DataFrame(result, columns=['store', 'sido-gu', 'address', 'phone'])
    
    # csv 저장
    hollys_df.to_csv('./day03/hollys_shop_info3.csv', index=True, encoding='utf8') 
    # 기본적으로 ./나 아무것도 안 붙이면 /폴더(가장 상위 폴더)에 저장된다. 
    # 만약 하위폴더에 저장하고 싶으면 ./day03/이나 day03/을 앞에 붙여줘야 한다.
    # /만 붙이면 상대경로가 아닌 절대경로가 되어서 아마 C폴더로 접근하는 것 같다. 
    print('저장 완료')
    
    del result[:] # result를 리셋한다.(지운다) 

if __name__ == '__main__':
    main()