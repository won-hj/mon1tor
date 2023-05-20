import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import csv
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.layouts import gridplot
import logging

'''
    path 경로의 파일들을 리스트나 개수로 반환
    option 0 : 파일 리스트 반환
           1 : 파일 개수 반환
'''
def get_files(path, option=0):
    import os

    dir_list = os.listdir(path)
    if option == 0:
        return (dir_list[:-1])
    else:
        return len(dir_list[:-1])

def get_location():
    return '../tool/'
# 1. 지금 디버그툴 깔려있지 않아서 적절한 것을 찾아야 한다.

# 딕셔너리에 {년도:데이터리스트} 로 저장
def get_csv():
    file = get_files(get_location(), 0)
    
    print(file, 'file') #비어있네
    set_figure = {} 
    
    for i in range(len(file)): #len(file)
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
    #get_csv()
    print(get_csv())