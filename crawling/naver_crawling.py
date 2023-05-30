# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
client_id = "lg542JOAVw0xKmjJ1Nlf"
client_secret = "BIjuZXEvKb"
encText = urllib.parse.quote("저출산 산업")
url = "https://openapi.naver.com/v1/search/blog?query=" + encText # JSON 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # XML 결과
