import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import csv
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.layouts import gridplot
import os
import sys
from configparser import ConfigParser

def get_files(path, option=0):
    dir_list = path 
    if option == 0:
        return os.listdir(dir_list)
    else:
        return len(os.listdir(dir_list))    

def get_location():
    cwd = os.getcwd() 
    path = os.path.join(cwd, '.\\config\\birth_death\\under\\')
    return path

# 딕셔너리에 {년도:데이터리스트} 로 저장
def get_csv():
    file = get_files(get_location(), 0)
    file_len = get_files(get_location(), 1)

    set_figure = {} 
    
    for i in range(file_len): 
        with open (get_location()+ str(2013+i) +'.csv', encoding='UTF-8') as f:
            reader = csv.reader(f)
            birth_death_data = []
            age_data = []
            for row in reader:
                if len(row) == 0 or row[0][0] == '#':
                    continue
                if row[0] == '출생아수' or row[0] == '사망자수':
                    birth_death_data.append(row)
                if row[0] == 'work_demo' or row[0] == 'nonwork_demo':
                    birth_death_data.append(row)
                elif row[0] == '생산가능인구(15-64)' or row[0] == '고령인구(65-)':
                    age_data.append(row)
                set_figure[file[i]] = [birth_death_data, age_data]
    return set_figure
#worknonwork
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
    p3 = figure(y_range=per_df['type'], title=Title(text="%d년 생산가능 인구 퍼센트와 \n고령인구 퍼센트(단위 : 백 명)"%int(year), align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"), height=500, width=500)
    p3.hbar(y='type', right='value', height=0.3, color=Spectral4[3], source=per_source)
    p3.xaxis.formatter = NumeralTickFormatter(format="0,0")
    p3.xaxis.formatter = xformatter
    p3.add_tools(HoverTool(tooltips=[("Type", "@type"), ("Value", "@value")])) #p1과 동일한 내용의 코드

    #퍼센트
    if branch is 'work_nonwork' and mark is 'under':
        plot.append(p3)


    #if p3 is None:
    #    plot.append(p1)
    #    plot.append(p2)

    #if  
    #plot.append(p3)
    layout = gridplot([plot])

    return layout 



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

        #get_csv 사용    
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




#===============================================================================================================
'''
    def test_location():
        return '../tool/'
    테스트할땐 경로 ./tool로 변경
    cp 적용 안함
'''
def test_csv():
    file = get_files('../tool/', 0)
    #print(len(file))
    set_figure = {} 
    
    for i in range(len(file)): 
        with open ('../config/birth\&death_data/under2022/'+ str(2013+i) +'data.csv', encoding='UTF-8') as f:
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
                set_figure[file[i]] = [birth_death_data, age_data]

    return set_figure


























if __name__ == "__main__":
    #print(list(test_csv().values())[0][0])
    #print(list(test_csv().values())[0][1])
    #print(test_csv().values())
    #print(get_files(test_location(), 0))
    '''
    ['2013data.csv', '2014data.csv', '2015data.csv', '2016data.csv', '2017data.csv', 
    '2018data.csv', '2019data.csv', '2020data.csv', '2021data.csv', '2022data.csv', 'CSV']
    -> ['2013data.csv', '2014data.csv', '2015data.csv', '2016data.csv', '2017data.csv', 
    '2018data.csv', '2019data.csv', '2020data.csv', '2021data.csv', '2022data.csv']

    '''
    #get_cp() #123 
    #print(get_location())
    #print(os.path.abspath('2013.csv'))
    #print(get_location())
    get_csv()
    #print(os.getcwd())
    #print(os.path.join(os.getcwd(), './../config/birth_death/under22/'))


"""
    #################################
parser = ConfigParser()
parser.read('./config/config.ini', encoding='utf-8')
#configparser 테스트
'''
    $ python PrintGraph.py 
    'config/birth_death/over2022'
    'config/birth_death/under2022'
    'config/work_nonwork/over2022'
    'config/work_nonwork/under2022'
'''
##################################
test = ['birthover', 'birthunder', 'workover', 'workunder']

def get_cp():
    
    for i in test:
        print(parser.get('config', i))
##################################

'''
    path 경로의 파일들을 리스트나 개수로 반환
    option 0 : 파일 리스트 반환
           1 : 파일 개수 반환
'''


"""

