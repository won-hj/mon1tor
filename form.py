from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from Models import User #Models.py 가져옴

class RegisterForm(FlaskForm): #비밀번호 유효성 검사
    userid = StringField('userid', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), EqualTo('password_2')]) #비밀번호 확인
    password_2 = PasswordField('repassword', validators=[DataRequired()])

class UserPassword(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        userid = form['userid'].data
        password = field.data

        usertable = User.query.filter_by(userid=userid).first()
        if usertable is None:
           flash('No user found with this userid')  # 에러 메시지 보여주기
           raise ValueError('No user found with this userid')
        elif not usertable.check_password(password):
            flash('Password is incorrect')  # 에러 메시지 보여주기
            raise ValueError('Password is incorrect')

class LoginForm(FlaskForm):       
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])