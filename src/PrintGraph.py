import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import csv
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.layouts import gridplot
import logging
import os

'''
    path 경로의 파일들을 리스트나 개수로 반환
    option 0 : 파일 리스트 반환
           1 : 파일 개수 반환
'''
def get_files(path, option=0):
    dir_list = path 
    if option == 0:
        return os.listdir(dir_list)[:-1]
    else:
        return len(os.listdir(dir_list)[:-1])

def get_location():
    cwd = os.getcwd()
    path = os.path.join(cwd, '.\\tool\\')
    return path

# 딕셔너리에 {년도:데이터리스트} 로 저장
def get_csv():
    file = get_files(get_location(), 0)

    set_figure = {} 
    
    for i in range(len(file)): 
        with open (get_location()+ str(2013+i) +'data.csv', encoding='UTF-8') as f:
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
    
'''
def test_location():
    return '../tool/'
테스트할땐 경로 ./tool로 변경
'''

def test_csv():
    file = get_files('../tool/', 0)
    #print(len(file))
    set_figure = {} 
    
    for i in range(len(file)): 
        with open ('../tool/'+ str(2013+i) +'data.csv', encoding='UTF-8') as f:
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
    print(list(test_csv().values())[0][0])
    print(list(test_csv().values())[0][1])
    #print(test_csv().values())
    #print(get_files(test_location(), 0))
    '''
    ['2013data.csv', '2014data.csv', '2015data.csv', '2016data.csv', '2017data.csv', 
    '2018data.csv', '2019data.csv', '2020data.csv', '2021data.csv', '2022data.csv', 'CSV']
    -> ['2013data.csv', '2014data.csv', '2015data.csv', '2016data.csv', '2017data.csv', 
    '2018data.csv', '2019data.csv', '2020data.csv', '2021data.csv', '2022data.csv']

    '''
    #print(get_files('../tool/', 0))
