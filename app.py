from flask import Flask, render_template, request
from crawling import naver_crawling

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
    
    news_html = naver_crawling.predict(age)
    return render_template('prediction.html', table=news_html, age=age)

if __name__ == "__main__":
    app.run()
