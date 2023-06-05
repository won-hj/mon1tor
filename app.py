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
import sys
app = Flask(__name__)

"""
@app.route에 설정된 '/' 로 접속하면 hello world 출력
localhost:5000/ 로 접속
"""
@app.route('/', methods=['GET'])
def hello():
    return render_template('demo.html')

#22~36년도의 그래프 한번에 출력
@app.route('/graph_example')
def graph_example():
    from src import PrintGraph as g #ImportError: attempted relative import with no known parent package 

    csv = g.get_csv()
    file_length = g.get_files(g.get_location(), 1)
    plot_list = []

    xformatter = NumeralTickFormatter(format="0,0") # x축 1000단위 ,형식 제공

    for i in range(1, file_length):
        birth_death_df = pd.DataFrame(list(csv.values())[i][0], columns=['type', 'value'])
        age_df = pd.DataFrame(list(csv.values())[i][1], columns=['type', 'value'])

        birth_death_source = ColumnDataSource(birth_death_df)
        age_source = ColumnDataSource(age_df)
        globals()['p{}'.format(i)] = figure(y_range=birth_death_df['type'], title=Title(text='%d년 출생아인구 수 사망자 수'%int(2013+(i-1)),align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
        globals()['p{}'.format(i)].hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=birth_death_source)
        globals()['p{}'.format(i)].xaxis.formatter = NumeralTickFormatter(format="0.0")
        globals()['p{}'.format(i)].xaxis.formatter = xformatter
        globals()['p{}'.format(i)].add_tools(HoverTool(tooltips=[("Type", "@Type"), ("Value", "@value")]))
        plot_list.append(globals()['p{}'.format(i)]) 

    #sys.stderr.write('graph_ex: ' + str(plot_list))
    layout = gridplot([plot_list])

    return json.dumps(json_item(layout, 'layout'))

#13~22년도의 그래프 각각 출력
@app.route('/testgraph') #보류
def testgraph():
    # 여기선 gridplot 만 가져와서 입력
    #from src.PastGraph import pastgraph 
    from src import PastGraph as pg

    mark = 'under' #over/under
    year = 2013
    graph = pg.pastgraph(mark)
    plot = graph.get_plot(year)


    birth_death_data = plot[0]
    age_data = plot[1]

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

    p2 = figure(y_range=age_df['type'], title=Title(text=year+"년 생산가능 인구와 \n고령인구 수(단위 : 백 명)", align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p2.hbar(y='type', right='value', height=0.3, color=Spectral4[2], source=age_source)
    p2.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p2.xaxis.formatter = xformatter
    p2.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드

    layout = gridplot([[p1, p2]])
    #self.plot = layout
    print(layout)
    return json.dumps(json_item(layout, 'test_layout'))
    #return str(plot) # None


@app.route('/testbd') #보류
def testbd():
    from src.transition import birthdeath
    bd = birthdeath.birthdeath('over')
    plot = bd.get_data(2013)

    #return json.dumps(json_item(plot, 'test_layout'))
    return str(plot) #None



#### 해결 - FactorRange must specify a unique list of categorical factors for an axis: duplicate factors found  ####
#해결되면 구분해서 화면에 띄워주기만 하면 된다.
@app.route('/testbdapp')
def testapp():
    import sys
    branch, mark, year = 'birth_death', 'under', 2013 #확인
    layout = get_plot(branch, mark, year)
    return json.dumps(json_item(layout, 'test_bdapp')) 

@app.route('/testwnwapp')
def testwnwapp():
    import sys
    #from prophet
    branch, mark, year = 'work_nonwork', 'under', 20132022
    #branch, mark, year = 'birth_death', 'under', 2014 #확인
    layout = get_plot(branch, mark, year)

    return json.dumps(json_item(layout, 'test_wnwapp')) 

#4개 케이스 테스트 

#다른 구조간 구분 - opencsv1 > 가로행
#                - opencsv2 > 세로행
def opencsv(branch ,mark, year):
    import csv, os

    cwd = os.getcwd() 
    path = os.path.join(cwd, '.\\config\\'+ branch +'\\'+mark+'\\')
    
    with open( path + str(year) + '.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        birth_death_data = []
        age_data = []

        if branch is 'birth_death':
            if mark is 'over':#over에서의 동작
                pass
            else: #under에서의 동작
                for row in reader:
                    if len(row) == 0 or row[0][0] == '#':
                        continue
                    if row[0] == '출생아수' or row[0] == '사망자수':
                        birth_death_data.append(row)
                    if row[0] == '생산가능인구(15-64)' or row[0] == '고령인구(65-)':
                        age_data.append(row)
                    if row[0] == 'births' or row[0] == 'deaths':
                        birth_death_data.append(row)
                    elif row[0] == 'work_demo' or row[0] == 'nonwork_demo':
                        age_data.append(row)
                

        elif branch is 'work_nonwork':
            temp1 = []
            temp2 = []
            mean = {}
            with open( path + str(year) + '.csv', encoding='utf-8') as f:
                reader = csv.reader(f)
                percent_data = []
                age_data = []

                #lenrow = len(row)
                #print('lenrow' + str(lenrow))

                if mark is 'over': #over 동작
                    for row in reader:
                        lenrow = len(row)
                        if row[0].isnumeric():
                            for i in range(1, 5):
                                temp1.append(row[i])
                    print('lenrow' + str(lenrow))
                    for i in range(4): #4개있어서 
                        temp2.append(temp1[2*i:2*(i+1)]) 
                    
                    for i in range(len(temp2)):
                        try:
                            mean['생산인구 수'] + temp2[i][2]
                            mean['노령인구 수'] + temp2[i][3]
                        except KeyError:
                            mean['생산인구 수'] = temp2[i][2]
                            mean['노령인구 수'] = temp2[i][3]
                    sys.stderr.write(str(mean))
                    pass
                else: #under
                    for row in reader:
                        if row[0].isnumeric():
                            for i in range(1, 5):
                                temp1.append(row[i])

                    for i in range(2022-2013):
                        temp2.append(temp1[4*i:4*(i+1)]) 
                
                sys.stderr.write(str(temp2))
                '''
                [ 
                ['73.4', '11.9', '3701', '602'], 
                ['73.4', '12.4', '3725', '627'], 
                ['73.4', '12.8', '3744', '654'], 
                ['73.4', '13.2', '3759', '675'], 
                ['73.2', '13.8', '3757', '706'], 
                ['72.9', '14.3', '3762', '736'], 
                ['72.7', '14.9', '3762', '768'], 
                ['72.1', '15.7', '3737', '815'], 
                ['71.6', '16.6', '3702', '857']
                ]
                -> [1]:
                '''
                for i in range(len(temp2)):
                    try:
                        mean['생산인구 퍼센트'] + temp2[i][0]
                        mean['노령인구 퍼센트'] + temp2[i][1]
                        mean['생산인구 수'] + temp2[i][2]
                        mean['노령인구 수'] + temp2[i][3]
                    except KeyError:
                        mean['생산인구 퍼센트'] = temp2[i][0]
                        mean['노령인구 퍼센트'] = temp2[i][1]
                        mean['생산인구 수'] = temp2[i][2]
                        mean['노령인구 수'] = temp2[i][3]
                sys.stderr.write(str(mean))

        percent_data = [['임시1', 1234],['임시2', 4567]]
    return [birth_death_data, age_data, percent_data]

def get_plot(branch, mark, year):
    import sys
    #year = 2013~2022/ 2022,2027,2032,2037/ 20132022
    #mark = under/over
    #branch = /birth_death/work_nonwork
    plot = []
    datalist = opencsv(branch, mark, year)
    xformatter = NumeralTickFormatter(format="0,0")

    bd_df = pd.DataFrame(datalist[0], columns=['type', 'value'])
    age_df = pd.DataFrame(datalist[1], columns=['type', 'value'])
    per_df = pd.DataFrame(datalist[2], columns=['type', 'value'])
    #sys.stderr.write('get_plot/'+ branch+mark +': '+str(datalist)) #testapp
    bd_source = ColumnDataSource(bd_df)
    age_source = ColumnDataSource(age_df)
    per_source = ColumnDataSource(per_df)
    #sys.stderr.write('\nget_plot/'+ branch+mark +': '+str(datalist[0]))
    #sys.stderr.write('\nget_plot/'+ branch+mark +': '+str(datalist[1]))
    #sys.stderr.write('\nget_plot/'+ branch+mark +': '+str(datalist[2]))

    #flag에 따라 결과값(p1, p2) 달라진다
    if True:
        pass

    p1 = figure(y_range=bd_df['type'], title=Title(text='%d년 출생아 수 사망자 수'%int(year), align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p1.hbar(y='type', right='value', height=0.3, color=Spectral4[1], source=bd_source)
    p1.xaxis.formatter = NumeralTickFormatter(format="0.0")
    p1.xaxis.formatter = xformatter
    p1.add_tools(HoverTool(tooltips=[("Type", "@Type"), ("Value", "@value")]))
    ####
    p2 = figure(y_range=age_df['type'], title=Title(text="%d년 생산가능 인구와 \n고령인구 수(단위 : 백 명)"%int(year), align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p2.hbar(y='type', right='value', height=0.3, color=Spectral4[2], source=age_source)
    p2.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p2.xaxis.formatter = xformatter
    p2.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드
    ####
    p3 = figure(y_range=per_df['type'], title=Title(text="2013~2022년 생산가능 인구와 \n고령인구 수(단위 : 백 명)", align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p3.hbar(y='type', right='value', height=0.3, color=Spectral4[3], source=per_source)
    p3.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p3.xaxis.formatter = xformatter
    p3.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드

    
    plot.append(p1)
    plot.append(p2)
    plot.append(p3)
    layout = gridplot([plot])

    return layout

if __name__ == '__main__':
    app.run()


