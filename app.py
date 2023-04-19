from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def hello():
    """
    @app.route에 설정된 '/' 로 접속하면 hello world 출력
    localhost:5000/ 로 접속
    """
    return 'hello world'


@app.route('/demo')
def demo():
    """
    @app.route에 설정된 '/demo'로 접속하면 demo.html 화면 출력
    localhost:5000/demo.html 로 접속
    """
    return render_template('demo.html')

if __name__ == '__main__':
    app.run()

