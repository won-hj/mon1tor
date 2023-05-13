import json

from flask import Flask, render_template
from jinja2 import Template

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN

app = Flask(__name__)

"""
@app.route에 설정된 '/' 로 접속하면 hello world 출력
localhost:5000/ 로 접속
"""
@app.route('/')
def hello():
    json1={'id':1, 'a':2}
    #테스트용 템플릿 
    return render_template('example.html')

@app.route('/test_example')
def example():
  from bokeh.plotting import figure
  from bokeh.resources import CDN
  from bokeh.embed import file_html

  #테스트용 수치 
  p = figure()
  p.circle([1,2], [3,4])

  item_text = json.dumps(json_item(p, "myplot"))

  return json.dumps(json_item(p, "myplot"))

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run()

