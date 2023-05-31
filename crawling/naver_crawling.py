import os
import sys
import urllib.request
import requests
#api 사용해서 불러오기
client_id = "lg542JOAVw0xKmjJ1Nlf"
client_secret = "mArt8cw08s"
url = "https://openapi.naver.com/v1/search/news.json" # JSON 결과

#display_num : 한 번에 표시할 검색 결과 개수 (default : 10 max : 100)
def keyword(key, display_num): #return 크롤링결과 json형식 / key : 검색 단어, display_num: 가져올 페이지 개수
    headers = {'X-Naver-Client-Id' : client_id,
               'X-Naver-Client-Secret' : client_secret}
    params = {'query': key,
              'display':display_num,
              'sort':'sim'} #sim:정확도 순으로 정렬(default)
    response = requests.get(url,params=params,headers=headers)
    response_json = response.json()
    if response.status_code != 200: 
        print(f"Error: {response.status_code}")
        print(response_json) 
        return 

    r = response_json.get('items',[])

    return r 
results = keyword("저출산 산업",10)

for result in results:
    print(results)

