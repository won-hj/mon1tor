## Contributor
|      김도현       |          원혁주         |       김을중         |                                                                                                               
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | 
|   <img width="160px" src="https://avatars.githubusercontent.com/u/74997120?s=400&v=4" />    |                      <img width="160px" src="https://avatars.githubusercontent.com/u/128560356?v=4" />    |                   <img width="160px" src="https://avatars.githubusercontent.com/u/127865678?v=4"/>   |
|   [@dozzzang](https://github.com/dozzzang)   |    [@won-hj, @1hjwon](https://github.com/won-hj)  | [@KimEulJoong](https://github.com/KimEulJoong)  |
|              컴퓨터공학과2학년                |            컴퓨터공학과3학년              |                 물리학과4학년                             |
|             sks020k@naver.com                |           won.hyeockju@gmail.com, whjbssc@gmail.com         |                 kimeuljoong97@gmail.com                           |                                           

## 프로젝트 소개
2023-1 오픈소스기초프로젝트 강의 프로젝트입니다. '예측'이라는 키워드에 저희가 생각한 주제는 한국의 저출산과 고령화 현상입니다. 한국의 저출산과 고령화 현상은 가속화 되고 있지만, 대중들의 인식은 그 속도를 따라가지 못하는 것에 아쉬움을 느껴 사람들에게 미래의 인구 변화를 체감시켜주고자 웹이 만들어졌습니다. MON2TOR에서는 회원기능과 미래의 인구구조 변화에 대해 그래프를 제공하고, 사용자의 나이에 따른 도움 될 정보를 기사 주소를 통해 제공해줍니다.

## 설치 방법
``` bash
$ git clone https://github.com/won-hj/mon2tor.git
$ cd ./MON2TOR
pip install bokeh==2.4.2
pip install flask==2.2.2
pip install pandas==1.5.3
pip install prophet==1.1.2
pip install Flask-SQLAlchemy==3.0.3
pip install Flask-WTF==1.1.1
pip install request==2.28.1
```
## 충돌 발생 시
```
pip uninstall holidays
pip install holidays==0.10.5.2
```
## 의존성
``` 
[Language]
python>=3.8.1
[Web Framework]
Flask==2.2.2
[Database]
Flask-SQLAlchemy==3.0.3
[Form Handling]
Flask-WTF==1.1.1
WTForms==3.0.1
[Data Visualization]
bokeh==2.4.2
[Data Analysis]
prophet==1.1.2
pandas==1.5.3
[HTTP Requests]
requests==2.28.1
```
## 사용 방법
``` 
app.py로 이동하여 $ python app.py
개발서버로 접속
웹 페이지 상단 우측을 이용하여 회원가입/로그인/로그아웃 가능
나이를 입력하면 예측에 대한 링크로 이동가능 아래 나오는 사진을 클릭하면 과거에 대한 링크로 이동가능
``` 
---
## 주요 기능

### ⭐ 사용자의 나이를 입력
- 사용자의 나이에 맞는 인구구조와 관련된 키워드의 기사 링크 제공
- 미래 인구구조에 대한 상호작용 그래프 제공

### ⭐️ 과거와 현재의 인구구조 그래프
- 미래 뿐만 아니라 과거와 현재의 인구구조 상호작용 그래프 제공

### ⭐️ 회원 기능
- 회원가입/로그인 기능을 제공하며 (인구구조 예측 그래프를 보고 각자의 의견을 공유할 수 있는 커뮤니티 기능 제공 미구현)

---
## License
```
MIT License

Copyright (c) 2023 MON2TOR

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
## 아키텍쳐
### 디렉토리 구조
```
|   .gitignore
|   activate
|   app.py : 개발 서버
|   db.sqlite : 회원 정보 DB
|   form.py : 비밀번호 유효성 검사
|   Models.py : DB구성,비밀번호해싱
|   README.md
|   LICENSE
|   dave_server.log
|
+---config : 서버에 넘길 파일과 데이터베이스 관련 폴더
|   |   config.ini
|   |
|   +---birth_death
|   |   +---over
|   |   |       2022.csv
|   |   |       2027.csv
|   |   |       2032.csv
|   |   |       2037.csv
|   |   |
|   |   \---under
|   |           2013.csv
|   |           2014.csv
|   |           2015.csv
|   |           2016.csv
|   |           2017.csv
|   |           2018.csv
|   |           2019.csv
|   |           2020.csv
|   |           2021.csv
|   |           2022.csv
|   |           2023.csv
|   |
|   +---prediction_graph : 서버에 넘길 미래 예측 그래프
|   |   +---birth_death
|   |   |   |   bdp20232027.py
|   |   |   |   bdp20282032.py
|   |   |   |   bdp20332037.py
|   |   |   |
|   |   |   \---__pycache__
|   |   |           bdp20232027.cpython-310.pyc
|   |   |           bdp20282032.cpython-310.pyc
|   |   |           bdp20332037.cpython-310.pyc
|   |   |
|   |   \---work_nonwork
|   |       |   wnwp20232027.py
|   |       |   wnwp20282032.py
|   |       |   wnwp20332037.py
|   |       |
|   |       \---__pycache__
|   |               wnwp20232027.cpython-310.pyc
|   |               wnwp20282032.cpython-310.pyc
|   |               wnwp20332037.cpython-310.pyc
|   |
|   \---work_nonwork
|       +---over
|       |       2022.csv
|       |       2027.csv
|       |       2032.csv
|       |       2037.csv
|       |
|       \---under
|               20132022.csv
|
+---crawling : 네이버 API를 이용한 크롤링 폴더
|   |   naver_crawling.py
|   |
|   \---__pycache__
|           naver_crawling.cpython-310.pyc
|
+---Data_pipeline : 예측에 들어가는 데이터 파이프라인화
|       2023-2027 csv 추출.py
|       2023-2027_csv추출,병합.py
|       2023-2027_workcsv추출,병합.py
|       2028-2032_csv추출,병합.py
|       2028-2032_workcsv추출,병합.py
|       2033-2037_csv추출,병합.py
|       2033-2037_workcsv추출,병합.py
|
+---past_graph : 과거 그래프 시각화
|   |   2013data_graph.py
|   |   2014data_graph.py
|   |   2015data_graph.py
|   |   2016data_graph.py
|   |   2017data_graph.py
|   |   2018data_graph.py
|   |   2019data_graph.py
|   |   2020data_graph.py
|   |   2021data_graph.py
|   |   2022data_graph.py
|   |   past_work_nonwork_graph.py
|   |
|   \---__pycache__
|           past_work_nonwork_graph.cpython-310.pyc
|
+---prediction_graph : 미래 그래프 
|   +---birth&death
|   |       2023-2027_graph.py
|   |       2028-2032_graph.py
|   |       2033-2037_graph.py
|   |
|   \---work&nonwork
|           2023-2027_graph.py
|           2028-2032_graph.py
|           2033-2037_graph.py
|
+---src
|   |   FilePath.py
|   |   PastGraph.py
|   |   PrintGraph.py
|   |   __init__.py
|   |
|   +---past_graph
|   |       2013data_graph.py
|   |       2014data_graph.py
|   |       2015data_graph.py
|   |       2016data_graph.py
|   |       2017data_graph.py
|   |       2018data_graph.py
|   |       2019data_graph.py
|   |       2020data_graph.py
|   |       2021data_graph.py
|   |       2022data_graph.py
|   |       __init__.py
|   |
|   +---transition
|   |       birthdeath.py
|   |       worknonwork.py
|   |       __init__.py
|   |
|   \---__pycache__
|           PrintGraph.cpython-310.pyc
|           __init__.cpython-310.pyc
|
+---static : JS,CSS,IMAGE
|   +---assets
|   |   \---demo
|   |           chart-area-demo.js
|   |           chart-bar-demo.js
|   |           chart-pie-demo.js
|   |           datatables-demo.js
|   |
|   +---css : 부트스트랩 css
|   |       styles.css
|   |
|   +---image
|   |       link1.PNG
|   |       link2.PNG
|   |       logo.png
|   |       LOGO2.PNG
|   |
|   \---js
|           bokeh-tables.min.js
|           bokeh-widgets.min.js
|           bokeh.min.js
|           js_to_server.py : bokeh를 외부에서 받아올 수 없어 내부에서 받아오기 시도(시도 자체는 성공했지만 렌더링에 실패)
|           scripts.js : index와 나이를 넘기는데 쓰이는 js파일
|
+---templates : 화면 구성
|       demo.html
|       example.html
|       index.html : 메인화면
|       login.html : 로그인화면
|       past_graph1.html : 과거 그래프 화면 좌측
|       past_graph2.html : 과거 그래프 화면 우측
|       prediction.html : 미래 그래프 화면 
|       register.html : 회원가입 화면
|
+---tool : 그래프 생성에 필요한 data
|   +---birth&death_data
|   |       -2022data.csv
|   |       -2027data.csv
|   |       -2032data.csv
|   |       -2036data.csv
|   |       -2037data.csv
|   |       2013data.csv
|   |       2014data.csv
|   |       2015data.csv
|   |       2016data.csv
|   |       2017data.csv
|   |       2018data.csv
|   |       2019data.csv
|   |       2020data.csv
|   |       2021data.csv
|   |       2022data.csv
|   |
|   \---work&nonwork_data
|           -2022_data.csv
|           -2027_data.csv
|           -2032_data.csv
|           -2036_data.csv
|           -2037_data.csv
|           2013-2022data.csv
``` 
