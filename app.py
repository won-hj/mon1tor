import json

from flask import Flask, render_template
from jinja2 import Template

from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
#from bokeh.sampledata.iris import flowers


app = Flask(__name__)

''' 가이드 예시 일부 
page = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
  {{ resources }}
</head>
<body>
  <div id="myplot"></div>
  <div id="myplot2"></div>
  <script>
  fetch('/plot')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item); })
  </script>
  <script>
  fetch('/plot2')
    .then(function(response) { return response.json(); })
    .then(function(item) { return Bokeh.embed.embed_item(item, "myplot2"); })
  </script>
</body>
""")
'''
@app.route('/')
def hello():
    """
    @app.route에 설정된 '/' 로 접속하면 hello world 출력
    localhost:5000/ 로 접속
    """
    json1={'id':1, 'a':2}
    return json1


#file_html 시 그림이 나오지만 json으로는 그림이 나오지 않음
#http://localhost:5000/demo_plot 접속 시 그림이 나와야 함(따로 템플릿 필요 없음)
@app.route('/demo_plot')
def demo_plot():
    """
    @app.route에 설정된 '/demo'로 접속하면 demo.html 화면 출력
    localhost:5000/demo.html 로 접속
    """
    from bokeh.plotting import figure
    from bokeh.embed import json_item, file_html

    plot =  figure()
    plot.circle([1,2,5], [3, 4, 8], size=20, color='navy', alpha=0.5)

    jsonfied_plot = json_item(model=plot, target='test_plot')

                                                        # '\'
    return json.dumps(jsonfied_plot, ensure_ascii=False, indent='\t') 
    #return file_html(models=[plot], resources=CDN, title="test_plot")

@app.route('/demo')
def demo():
    return render_template('demo.html')


if __name__ == '__main__':
    app.run()

