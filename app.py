import json

from flask import Flask, render_template
from jinja2 import Template

from bokeh.embed import json_item, file_html 
from bokeh.plotting import figure
from bokeh.resources import CDN

from bokeh.client import pull_session
from bokeh.embed import server_session

app = Flask(__name__)

"""
@app.route에 설정된 '/' 로 접속하면 hello world 출력
localhost:5000/ 로 접속
"""
@app.route('/', methods=['GET'])
def hello():
    #테스트용 템플릿
    '''
    with pull_session(url='http://127.0.0.1:5006/demo') as session:
        # update or customize that session cusromize session이라는데 문서를 더 보기
        session.document.roots[0].children[1].title.text = "일단 따라해보기; root[여기랑].children[여기의 의미를 모르겠다]"
        # generate a script to load the customized session
        script = server_session(session_id=session.id, url='http://localhost:5006/demo')
        # use the script in the rendered page
        return render_template('example.html', script=script, template="Flask")
    '''
    #script = 
    #return render_template('example.html', script=script, template='Flask')
    return render_template('demo.html')


@app.route('/graph_example')
def graph_example():
    #from past_graph import *
    #gridplot = past_graph.2013data_graph.layout
    import pandas as pd
    from bokeh.plotting import figure, output_file, show
    from bokeh.models import ColumnDataSource, HoverTool, Title
    from bokeh.palettes import Spectral4
    import csv
    from bokeh.models import BasicTickFormatter, NumeralTickFormatter
    from bokeh.layouts import gridplot

    with open('./tool/2013data.csv', encoding='UTF-8') as f:        # csv모듈의 reader함수를 이용해 csv파일을 읽어들여 각 행을 구분
        reader = csv.reader(f)
        birth_death_data = []
        age_data = []
        for row in reader:
            if len(row) == 0 or row[0][0] == '#':
                continue
            if row[0] == '출생아수' or row[0] == '사망자수':
                birth_death_data.append(row)
            elif row[0] == '생산가능인구(15-64)' or row[0] == '고령인구(65-)':
                age_data.append(row)

    birth_death_df = pd.DataFrame(birth_death_data, columns=['type', 'value']) #pandas 모듈을 이용해 gridplot으로 나타내기 위해 df 두개 생성
    age_df = pd.DataFrame(age_data, columns=['type', 'value'])

    birth_death_source = ColumnDataSource(birth_death_df) #bokeh에서 지원하는 ColumnDataSource를 이용해 시각적인 요소를 구성하는데 기반
    age_source = ColumnDataSource(age_df)

    xformatter = NumeralTickFormatter(format="0,0") # x축 1000단위 ,형식 제공
    p1 = figure(y_range=birth_death_df['type'], title=Title(text="2013년 출생아 수 사망자 수", align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p1.hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source) #첫번째 가로 막대 그래프
    p1.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p1.xaxis.formatter = xformatter
    p1.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) # 마우스를 갖다대면 type과 value를 시각화

    p2 = figure(y_range=age_df['type'], title=Title(text="2013년 생산가능 인구와 \n고령인구 수(단위 : 백 명)", align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p2.hbar(y='type', right='value', height=0.3, color=Spectral4[2], source=age_source)
    p2.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p2.xaxis.formatter = xformatter
    p2.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드

    layout = gridplot([[p1, p2]])

    #show(layout)

    return json.dumps(json_item(layout, 'layout'))
    #return render_template('example.html')


@app.route('/test_example')
def test_example():
  #테스트용 수치 
  p = figure()
  p.circle([2,4], [3,4])

  item_text = json.dumps(json_item(p, "myplot"))

  return json.dumps(json_item(p, "myplot"))

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run()

