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
        self.set_password(password)
    
    def set_password(self, password): # 비밀번호를 해싱해서 저장
        self.password = generate_password_hash(password)
 
    def check_password(self, password): # return compare(해싱된 비밀번호,입력된 비밀번호)
        return check_password_hash(self.password, password)
