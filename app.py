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
    return render_template('index.html')

#기본 그래프 출력, route는 확인용 
#src/print_graph() 만들어서 해당 내용 가져오기
# web에있는거 분석해보고 template으로 옮겨서 적용시켜보기
@app.route('/graph_example')
def graph_example():
    from src import print_graph as g #ImportError: attempted relative import with no known parent package 

    csv = g.get_csv()
    file_length = g.get_files(g.get_location(), 1)
    plot_list = []
    #13년도에만 적용된다 -> 전체 데이터로 수정
    # 딕셔너리를 파일에 대해 구분한 다음 각 플롯에 맞춰 리스트로 만든 후 gridplot에 넣는다
    #birth_death_df = pd.DataFrame(birth_death_data, columns=['type', 'value']) #pandas 모듈을 이용해 gridplot으로 나타내기 위해 df 두개 생성
    #age_df = pd.DataFrame(age_data, columns=['type', 'value'])

    #일단 딕셔너리 구조 고려 안하고 ...  


    #기본은 파일 하나에 하나씩 불러들여서 데이터프레임을 만든다
    #지금할건 여러개를 불러들이기 때문에 맞춰서 해야한다
    #If no argument is given, the constructor creates a new empty list. The argument must be an iterable if specified. 라고한다
    '''    birth_death_df = pd.DataFrame(list(csv.values())[0], columns=['type', 'value'])
        age_df = pd.DataFrame(list(csv.values()[1]), columns=['type', 'value'])
        
        birth_death_source = ColumnDataSource(birth_death_df) #bokeh에서 지원하는 ColumnDataSource를 이용해 시각적인 요소를 구성하는데 기반
        age_source = ColumnDataSource(age_df)
    '''
    xformatter = NumeralTickFormatter(format="0,0") # x축 1000단위 ,형식 제공

    for i in range(1, file_length):
        birth_death_df = pd.DataFrame(list(csv.values())[i][0], columns=['type', 'value'])
        age_df = pd.DataFrame(list(csv.values())[i][1], columns=['type', 'value'])

        birth_death_source = ColumnDataSource(birth_death_df)
        age_source = ColumnDataSource(age_df)
        #(g.get_files[i-1][0:4])
        globals()['p{}'.format(i)] = figure(y_range=birth_death_df['type'], title=Title(text='%d년 출생아 수 사망자 수'%int(i+2013-1),align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
        globals()['p{}'.format(i)].hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source)
        globals()['p{}'.format(i)].xaxis.formatter = NumeralTickFormatter(format="0.0")
        globals()['p{}'.format(i)].xaxis.formatter = xformatter
        globals()['p{}'.format(i)].add_tools(HoverTool(tooltips=[("Type", "@Type"), ("Value", "@value")]))
        plot_list.append(globals()['p{}'.format(i)]) 
        '''
        #globals()['p{}'.format(i)] = figure(y_range=birth_death_df['type'], title=Title(text='%d년 출생아 수 사망자 수'%g.get_files[i-1][0:4]))

        
        '''

    #p1 = figure(y_range=birth_death_df['type'], title=Title(text="%d년 출생아 수 사망자 수"%csv, align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    #p1.hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source) #첫번째 가로 막대 그래프
    #p1.xaxis.formatter = NumeralTickFormatter(format="0,0")
    #p1.xaxis.formatter = xformatter
    #p1.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) # 마우스를 갖다대면 type과 value를 시각화

    #p2 = figure(y_range=age_df['type'], title=Title(text="2013년 생산가능 인구와 \n고령인구 수(단위 : 백 명)", align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    #p2.hbar(y='type', right='value', height=0.3, color=Spectral4[2], source=age_source)
    #p2.xaxis.formatter = NumeralTickFormatter(format="0,0")
    #p2.xaxis.formatter = xformatter
    #p2.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드
    
    #layout = gridplot([[p1, p2]])
    layout = gridplot([plot_list])
    #show(layout)

    return json.dumps(json_item(layout, 'layout'))
    #return render_template('example.html')

#csv 결과값 출력 예시
@app.route('/csv')
def csv():
    from src import print_graph as p
    return json.dumps(p.get_csv(), ensure_ascii=False).encode('utf8')


#출력예시 - localhost:5000/demo 접속 시 그래프 출력, /pastgraph 접속 시 jsondump 출력
@app.route('/pastgraph')
def pastgraph():
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
    p1 = figure(y_range=birth_death_df['type'], title=Title(text="%d년 출생아 수 사망자 수"%2013, align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
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
    return json.dumps(json_item(layout, 'layout'))


@app.route('/test_example')
def test_example():
  #테스트용 수치 
  '''
  p = figure()
  p.circle([2,4], [3,4])

  item_text = json.dumps(json_item(p, "myplot"))
  '''
  return json.dumps(json_item(p, "myplot"))

@app.route('/demo')
def demo():
    return render_template('demo.html')

if __name__ == '__main__':
    app.run()

