import json
from bokeh.layouts import gridplot
from flask import Flask, render_template
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
import pandas as pd
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
'''
app = Flask(__name__)

"""
@app.route에 설정된 '/' 로 접속하면 hello world 출력
localhost:5000/ 로 접속
"""
@app.route('/', methods=['GET'])
def hello():
    return render_template('index.html')

@app.route('/graph_example')

def graph_example():
    from src import PrintGraph as g #ImportError: attempted relative import with no known parent package 

    csv = g.get_csv()
    file_length = g.get_files(g.get_location(), 1)
    plot_list = []

    xformatter = NumeralTickFormatter(format="0,0") # x축 1000단위 ,형식 제공

    for i in range(1, file_length):
        birth_death_df = pd.DataFrame(list(csv.values())[i][0], columns=['type', 'value'])
        age_df = pd.DataFrame(list(csv.values())[i][1], columns=['type', 'value'])

        birth_death_source = ColumnDataSource(birth_death_df)
        age_source = ColumnDataSource(age_df)
        globals()['p{}'.format(i)] = figure(y_range=birth_death_df['type'], title=Title(text='%d년 출생아 수 사망자 수'%int(i+2013-1),align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
        globals()['p{}'.format(i)].hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source)
        globals()['p{}'.format(i)].xaxis.formatter = NumeralTickFormatter(format="0.0")
        globals()['p{}'.format(i)].xaxis.formatter = xformatter
        globals()['p{}'.format(i)].add_tools(HoverTool(tooltips=[("Type", "@Type"), ("Value", "@value")]))
        plot_list.append(globals()['p{}'.format(i)]) 


<<<<<<< HEAD
=======
        >>>>>>> b86282b076e0319ab97966a988e57f494c429232
    layout = gridplot([plot_list])

    return json.dumps(json_item(layout, 'layout'))

if __name__ == '__main__':
    app.run()
'''
import os
from flask import request, redirect
from flask_sqlalchemy import SQLAlchemy
from Models import db
from Models import User
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello World!'

@app.route('/register', methods=['GET','POST']) #GET(정보보기), POST(정보수정) 메서드 허용
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid')
        email = request.form.get('email')
        password = request.form.get('password')
        password_2 = request.form.get('password')

        if not(userid and email and password and password_2):
            return "입력되지 않은 정보가 있습니다"
        elif password != password_2:
            return "비밀번호가 일치하지 않습니다"
        else:
            usertable=User() #user_table 클래스
            usertable.userid = userid
            usertable.email = email
            usertable.password = password
            
            db.session.add(usertable)
            db.session.commit()
            return "회원가입 성공"
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

    app.run(host="127.0.0.1", port=5000, debug=True)