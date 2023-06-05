import csv
import json
import math
from bokeh.layouts import gridplot
from flask import Flask, render_template
from bokeh.embed import json_item
from bokeh.plotting import figure
from bokeh.resources import CDN
import pandas as pd
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4


from config.prediction_graph.birth_death import bdp20232027, bdp20282032
from config.prediction_graph.work_nonwork import wnwp20232027, wnwp20282032
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
    from src import PastGraph as pg

    mark = 'under' #over/under
    year = 2022
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

    print(layout)
    return json.dumps(json_item(layout, 'test_layout'))


@app.route('/testbd') #보류
def testbd():
    from src.transition import birthdeath
    bd = birthdeath.birthdeath('over')
    plot = bd.get_data(2013)

    #return json.dumps(json_item(plot, 'test_layout'))
    return str(plot) #None

################### 13~22년도 과거 통계 그래프
@app.route('/testbdapp')
def testapp():
    import sys
    branch, mark, year = 'birth_death', 'over', 2037 #확인
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
################### 13~27년도 미래 추이 그래프
@app.route('/testpredapp')
def test_predict():
    from config.prediction_graph.birth_death import bdp20232027 as g

    data = pd.read_csv('./tool/birth&death_data/-2022data.csv')
    p = g.ForecastPlotter(data, ['births', 'deaths'], '2023-2027')

    plot = p.plot()

    #return render_template()
    return json.dumps(json_item(plot, 'prelayout1'))

##################의견구하기########################
@app.route('/testallbdpred')
def test_prebdall():
    from config.prediction_graph.birth_death import bdp20332037, bdp20232027, bdp20282032


    data1, data2, data3 = pd.read_csv('./tool/birth&death_data/-2022data.csv'), pd.read_csv('./tool/birth&death_data/-2027data.csv'), pd.read_csv('./tool/birth&death_data/-2032data.csv')

    p1, p2, p3 = bdp20232027.ForecastPlotter(data1, ['births', 'deaths'], '2023-2027'), bdp20282032.ForecastPlotter(data2, ['births', 'deaths'], '2028-2032'), bdp20332037.ForecastPlotter(data3, ['births', 'deaths'], '2033-2037')

    plot1, plot2, plot3 = p1.plot(), p2.plot(), p3.plot()

    #layout = ([plot1, plot2, plot3])
    #layout = [plot1, plot2, plot3]

    return json.dumps(json_item(plot2, 'testallbdpredict'))

#TypeError: Converting from datetime64[ns] to int32 is not supported. Do obj.astype('int64').astype(dtype) instead
@app.route('/testallwnwpred')
def test_prewnwall():
    from config.prediction_graph.work_nonwork import wnwp20332037, wnwp20282032, wnwp20332037


    data1, data2, data3 = pd.read_csv('./tool/work&nonwork_data/-2022_data.csv'), pd.read_csv('./tool/work&nonwork_data/-2027_data.csv'), pd.read_csv('./tool/work&nonwork_data/-2032_data.csv')

    p1, p2, p3 = wnwp20232027.ForecastPlotter(data1, ['work_demo', 'nonwork_demo'], '2023-2027 생산가능인구/생산불가능인구 변화'), wnwp20282032.ForecastPlotter(data2, ['work_demo', 'nonwork_demo'], '2028-2032 생산가능인구/생산불가능인구 변화'), wnwp20332037.ForecastPlotter(data3, ['work_demo', 'nonwork_demo'], '2033-2037 생산가능인구/생산불가능인구 변화')

    plot1, plot2, plot3 = p1.plot(), p2.plot(), p3.plot()

    #layout = [plot1, plot2, plot3]

    return json.dumps(json_item(plot1, 'testallwnwpredict'))
######################################3
############################################
#테스트용 
@app.route('/testwnwpredict')
def test_prewnw():
    from config.prediction_graph.work_nonwork import wnwp20332037, wnwp20282032, wnwp20332037


    data1, data2, data3 = pd.read_csv('./tool/work&nonwork_data/-2022_data.csv'), pd.read_csv('./tool/work&nonwork_data/-2027_data.csv'), pd.read_csv('./tool/work&nonwork_data/-2032_data.csv')

    p1, p2, p3 = wnwp20232027.ForecastPlotter(data1, ['work_demo', 'nonwork_demo'], '2023-2027 생산가능인구/생산불가능인구 변화'), wnwp20282032.ForecastPlotter(data2, ['work_demo', 'nonwork_demo'], '2028-2032 생산가능인구/생산불가능인구 변화'), wnwp20332037.ForecastPlotter(data3, ['work_demo', 'nonwork_demo'], '2033-2037 생산가능인구/생산불가능인구 변화')

    plot1, plot2, plot3 = p1.plot(), p2.plot(), p3.plot()

    return json.dumps(json_item(plot1, 'testwnwpredict'))
@app.route('/example')
def example():
    return render_template('example.html')
#################################################################################3

#4개 케이스 테스트 - 확인
def opencsv(branch ,mark, year):
    import csv, os

    cwd = os.getcwd() 
    path = os.path.join(cwd, '.\\config\\'+ branch +'\\'+mark+'\\')
    
    birth_death_data = []
    age_data = []
    percent_data = []

    if branch is 'birth_death':
        if mark is 'over':#over에서의 동작
            birth_death_data = get_dfdata(flag=0, branch=branch, path=path, year=year)
                    
        else: #under에서의 동작
            with open( path + str(year) + '.csv', encoding='utf-8') as f:
                reader = csv.reader(f)

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
        if mark == 'over':
            age_data = get_dfdata(flag=0, branch=branch, path=path, year=year)
            pass
        else:
            percent_data = get_dfdata(flag=1, branch=branch, path=path, year=year)
            pass

        #age_data, percent_data
    return [birth_death_data, age_data, percent_data]

def get_plot(branch, mark, year):
    plot = []
    datalist = opencsv(branch, mark, year)
    xformatter = NumeralTickFormatter(format="0,0")

    bd_df = pd.DataFrame(datalist[0], columns=['type', 'value'])
    age_df = pd.DataFrame(datalist[1], columns=['type', 'value'])
    per_df = pd.DataFrame(datalist[2], columns=['type', 'value'])

    bd_source = ColumnDataSource(bd_df)
    age_source = ColumnDataSource(age_df)
    per_source = ColumnDataSource(per_df)

    #조건만들기 
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
    p3 = figure(y_range=per_df['type'], title=Title(text="%d년 생산가능 인구와 \n고령인구 수(단위 : 백 명)"%int(year), align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p3.hbar(y='type', right='value', height=0.3, color=Spectral4[3], source=per_source)
    p3.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p3.xaxis.formatter = xformatter
    p3.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드

    
    plot.append(p1)
    plot.append(p2)
    plot.append(p3)
    layout = gridplot([plot])

    return layout

def get_dfdata(flag, branch, path, year): #flag 1: 4, 0:2
    temp1, temp2 = [], []
    global mean
    mean = {}
    return_data = []
    type1, type2, type3, type4 = '', '', '', ''

    if flag == 1: #wnw/under
        sep = 4
        type1, type2, type3, type4 = '생산인구 퍼센트', '노령인구 퍼센트', '생산인구 수', '노령인구 수'
    elif flag == 0:#etc
        sep = 2
        if branch == 'birth_death':
             type1, type2 = '출생아 수', '사망자 수'
        else:
            type1, type2 = '생산인구 수', '노령인구 수'
        
    with open( path + str(year) + '.csv', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].isnumeric():
                for i in range(1, sep+1):
                    temp1.append(row[i])
        for i in range(int(len(temp1)/sep)): #ex)2022-2013+1                        
            temp2.append(temp1[sep*i:sep*(i+1)])  #확인        
        
        for i in range(0, 10): #2022-2013
            if sep == 2:
                try:
                    mean[type1] += round(float(temp2[i][0]))
                    mean[type2] += round(float(temp2[i][1]))
                except KeyError:
                    mean[type1] = round(float(temp2[i][0]))
                    mean[type2] = round(float(temp2[i][1]))
            elif sep == 4:
                try:
                    mean[type1] += round(float(temp2[i][0]))
                    mean[type2] += round(float(temp2[i][1]))
                    mean[type3] += round(float(temp2[i][2]))
                    mean[type4] += round(float(temp2[i][3]))
                except KeyError:
                    mean[type1] = round(float(temp2[i][0]))
                    mean[type2] = round(float(temp2[i][1]))
                    mean[type3] = round(float(temp2[i][2]))
                    mean[type4] = round(float(temp2[i][3]))

    try:
        mean[type1] /= 10
        mean[type2] /= 10
        mean[type3] /= 10
        mean[type4] /= 10
    except KeyError:
        mean[type1] /= 10
        mean[type2] /= 10
         
    return_data = list(mean.items())
    return return_data

if __name__ == '__main__':
    app.run()


