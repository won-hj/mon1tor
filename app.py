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


if __name__ == "__main__":
    app.run(debug=True)
