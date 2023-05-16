import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import csv
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.layouts import gridplot

'''
    path 경로의 파일들의 개수를 리스트로 반환
'''
def get_files(path):
    import os

    dir_list = os.listdir(path)
    return (dir_list[:-1])


def get_csv():
    f = (get_files('../tool'))
    print(f, len(f))
    '''   
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
    '''
if __name__ == "__main__":
    get_csv()
    