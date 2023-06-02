from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() #SQLAlchemy 인스턴스 생성

class User(db.Model): #데이터 모델(SQL table)을 나타내는 객체
    __tablename__ = 'user_table' #테이블 이름
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), unique=True, nullable=False)
    userid = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(8), nullable=False)

    def __init__(self, email, password): #User클래스 생성자
        self.email = email