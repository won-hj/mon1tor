import os
import re
import sys
import urllib.request
from matplotlib import pyplot as plt
import requests
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

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

def info(places): #return column,row형식의 dtf
    PubDate = []
    Title = []
    Link = []
    Description = []

    for place in places:

        PubDate.append(place['pubDate'])
        Title.append(place['title'])
        Link.append(place['link'])
        Description.append(place['description'])

    ar = np.array([PubDate, Title, Link, Description]).T 
    dtf = pd.DataFrame(ar, columns=['PubDate','Title','Link','Description'])
    return dtf

def basic_clear(text): # return 불필요한 기호 제거 text
    for i in range(len(text)) :
        text[i] = text[i].replace('<b>',' ')
        text[i] = text[i].replace('</b>',' ')
        text[i] = text[i].replace('&apos;',' ')
        text[i] = text[i].replace('&quot;',' ')
    return text

def extract_word(text): #return 특수기호 제거 result
    hangul = re.compile('[^가-힣0-9]')
    result = hangul.sub(' ',text)
    return result

@app.route('/predict', methods=['POST'])
def predict():
    age = int(request.form['age'])
    key = None
    if age >= 15 and age < 17:
        key = ['저출산', '학교 인구 변화']
    elif age >= 17 and age < 19:
        key = ['대학교']
    elif age >= 19 and age < 25:
        key = ['저출산 산업','고령화 산업']
    elif age >= 25 and age < 29:
        key = ['실버 산업','고령화']
    elif age >= 29 and age < 35:
        key = ['고령화 사업','저출산 사업']
    elif age >= 35 and age < 45:
        key = ['고령화 변화','저출산 변화']
    elif age >= 45 and age < 65:
        key =['실버 산업','인구 변화']

    news_all = pd.DataFrame(columns=['PubDate','Title','Link','Description'])
    for k in key:

        search = keyword(k, 5)
        news = info(search)
        basic_clear(news['Title'])
        basic_clear(news['Description'])
        length = len(news['Title'])-1

        for i in range(length):
            if news['Title'].iloc[i][:8] == news['Title'].iloc[i+1][:8]:
                news['Title'].iloc[i] = np.NaN
        news.dropna(inplace=True)

        for i in range(len(news['Title'])):
            news['Title'].iloc[i] = extract_word(news['Title'].iloc[i])
            news['Description'].iloc[i] = extract_word(news['Description'].iloc[i])

        news['Link'] = '<a href="'+ news['Link'] + '">링크</a>'
        news_all = pd.concat([news_all, news])

    news_html = news_all.to_html(escape=False)

    return render_template('prediction.html', table=news_html)