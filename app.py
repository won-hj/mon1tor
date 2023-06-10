import csv
import json
import math
from bokeh.layouts import gridplot
from flask import Flask, render_template
from bokeh.embed import json_item, autoload_static, file_html, components
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from flask import request
import pandas as pd
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import sys

from config.prediction_graph.birth_death import bdp20232027, bdp20282032
from config.prediction_graph.work_nonwork import wnwp20232027, wnwp20282032

from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from Models import db
from Models import User
from form import RegisterForm, LoginForm
from flask_wtf.csrf import CSRFProtect
from crawling import naver_crawling
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

if not app.debug: 
    # 즉 debug=true면 이는 false로서 아래 함수가 돌아간다.
    # 실제 상용화단계에서 로깅을 진행해라는 의미이다
    import logging
    from logging.handlers import RotatingFileHandler  
    # logging 핸들러에서 사용할 핸들러를 불러온다.
    file_handler = RotatingFileHandler(
        'dave_server.log', maxBytes=2000, backupCount=10)
    file_handler.setLevel(logging.CRITICAL)  
    # 어느 단계까지 로깅을 할지를 적어줌
    # app.logger.addHandler() 에 등록시켜줘야 app.logger 로 사용 가능
    app.logger.addHandler(file_handler)
 

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def register():
    form = RegisterForm()
    if form.validate_on_submit(): #내용 채우지 않은 항목이 있는지까지 체크
        userid = form.data.get('userid')
        email = form.data.get('email')
        password = form.data.get('password')

        usertable = User(userid, email, password) 

        db.session.add(usertable) #DB저장
        db.session.commit() #변동사항 반영
        
        return "회원가입 성공" 
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            userid = form.data.get('userid')
            user = User.query.filter_by(userid=userid).first()  # 사용자 ID로 데이터베이스 검색

            if not user:  # 사용자 정보가 데이터베이스에 없는 경우
                flash('No user found with this userid')
                return redirect('/login')

            session['userid'] = userid
            return redirect('/')
        except ValueError:
            return redirect('/login')  # ValueError 발생 시 로그인 페이지로 리다이렉트
    return render_template('login.html', form=form)
 
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

if __name__ == "__main__":
    #데이터베이스---------
    basedir = os.path.abspath(os.path.dirname(__file__)) #현재 파일이 있는 디렉토리 절대 경로
    dbfile = os.path.join(basedir, 'db.sqlite') #데이터베이스 파일을 만든다

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True #커밋=DB반영
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #추가 메모리를 사용하므로 꺼둔다

#    db = SQLAlchemy() #SQLAlchemy를 사용해 데이터베이스 저장
    db.init_app(app) #app설정값 초기화
    db.app = app #Models.py에서 db를 가져와서 db.app에 app을 명시적으로 넣는다
    with app.app_context():
        db.create_all() #db 생성

@app.route('/past_graph1')
def past_graph1():
    return render_template('past_graph1.html')

@app.route('/past_graph2')
def past_graph2():
    return render_template('past_graph2.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    age = None
    if request.method == 'POST':
        age = int(request.form.get('age', None))
    elif request.method == 'GET':
        age = int(request.args.get('age', None))

    if age is None:
        return render_template('prediction.html')
    
    news_descriptions = naver_crawling.predict(age)

    return render_template('prediction.html', descriptions=news_descriptions, age=age)
###########################
@app.route('/pred2327')
def pred2327():
    from config.prediction_graph.birth_death import bdp20232027 as g

    data = pd.read_csv('./tool/birth&death_data/-2022data.csv')
    p = g.ForecastPlotter(data, ['births', 'deaths'], '2023-2027')

    plot = p.plot()

    return json.dumps(json_item(plot, 'pred2327'))
@app.route('/pred2832')
def pred2832():
    from config.prediction_graph.birth_death import bdp20282032 as g

    data = pd.read_csv('./tool/birth&death_data/-2027data.csv')
    p = g.ForecastPlotter(data, ['births', 'deaths'], '2028-2032')

    plot = p.plot()

    return json.dumps(json_item(plot, 'pred2832'))
@app.route('/pred3337')
def pred3337():
    from config.prediction_graph.birth_death import bdp20332037 as g

    data = pd.read_csv('./tool/birth&death_data/-2032data.csv')
    p = g.ForecastPlotter(data, ['births', 'deaths'], '2033-2037')

    plot = p.plot()

    return json.dumps(json_item(plot, 'pred3337'))

@app.route('/pred20232027')
def pred20232027():
    from config.prediction_graph.work_nonwork import wnwp20232027 as g
    data = pd.read_csv('./tool/work&nonwork_data/-2022_data.csv')

    forecast_plotter = g.ForecastPlotter(data, ['work_demo', 'nonwork_demo'], '2023-2027 생산가능인구/생산불가능인구 변화')
    plot = forecast_plotter.plot()

    return json.dumps(json_item(plot, 'pred20232027'))

@app.route('/pred20282032') 
def pred20282032():
    from config.prediction_graph.work_nonwork import wnwp20282032 as g
    data = pd.read_csv('./tool/work&nonwork_data/-2027_data.csv')

    forecast_plotter = g.ForecastPlotter(data, ['work_demo', 'nonwork_demo'], '2028 - 2032 생산가능인구/생산불가능인구 변화')
    plot = forecast_plotter.plot()

    return json.dumps(json_item(plot, 'pred20282032'))

@app.route('/pred20332037') 
def pred20332037():
    from config.prediction_graph.work_nonwork import wnwp20332037 as g
    data = pd.read_csv('./tool/work&nonwork_data/-2032_data.csv')

    forecast_plotter = g.ForecastPlotter(data, ['work_demo', 'nonwork_demo'], '2033 - 2037 생산가능인구/생산불가능인구 변화')
    plot = forecast_plotter.plot()

    return json.dumps(json_item(plot, 'pred20332037'))


    from config.prediction_graph.birth_death import bdp20232027 as g

    data = pd.read_csv('./tool/birth&death_data/-2022data.csv')
    p = g.ForecastPlotter(data, ['births', 'deaths'], '2023-2027')

    plot = p.plot()

    return json.dumps(json_item(plot, 'pred2327'))
#13~22년도 한번에 출력
@app.route('/pastgraph1')
def pastgraph1():
    from src import PrintGraph as g 

    csv = g.get_csv()
    file_length = g.get_files(g.get_location(), 1)
    plot_list = []

    xformatter = NumeralTickFormatter(format="0,0") # x축 1000단위 ,형식 제공

    for i in range(1, file_length):
        birth_death_df = pd.DataFrame(list(csv.values())[i][0], columns=['type', 'value'])
        age_df = pd.DataFrame(list(csv.values())[i][1], columns=['type', 'value'])

        birth_death_source = ColumnDataSource(birth_death_df)
        age_source = ColumnDataSource(age_df)
        globals()['p{}'.format(i)] = figure(y_range=birth_death_df['type'], title=Title(text='%d년 출생아인구 수 사망자 수'%int(2013+(i-1)),align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
        globals()['p{}'.format(i)].hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source)
        globals()['p{}'.format(i)].xaxis.formatter = NumeralTickFormatter(format="0.0")
        globals()['p{}'.format(i)].xaxis.formatter = xformatter
        globals()['p{}'.format(i)].add_tools(HoverTool(tooltips=[("Type", "@Type"), ("Value", "@value")]))
        plot_list.append(globals()['p{}'.format(i)]) 

    layout = gridplot(plot_list, ncols=3)
    script, div = components(layout)
    return json.dumps(json_item(layout, 'pastgraph1'))
    #return render_template("prediction.html", script=script, div=div)

#13~22년도 pastgraph2
@app.route('/pastgraph2')
def pastgraph2():
    from past_graph.past_work_nonwork_graph import create_graph as g
    df = pd.read_csv('./tool/work&nonwork_data/2013-2022data.csv')
    df['Year'] = df['Year'].astype(str) 

    columns_titles_colors = [
        ('work_percent', '생산인구(%):15-64세', Spectral4[1]),
        ('nonwork_percent', '고령인구(%):65세 이상', Spectral4[2]),
    ]

    description = '*대한민국 전체 인구가 100%라고 가정했을 때 비율<br>*지방 중소도시 : 50만 이하의 인구<br>*생산인구 1%당 약 16만명 감소 생산인구로만 구성된 약 1개 중소도시 삭제<br>*고령인구 1%당 약 73만명 증가 고령인구로만 구성된 약 1개 중소도시 생성'
    layout = g(df, columns_titles_colors, description) 
    return json.dumps(json_item(layout, 'pastgraph2'))

if __name__ == "__main__":
    app.run(debug=True)
