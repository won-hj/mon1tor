from typing import Any
import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import csv
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.layouts import gridplot
import os
import sys

#config/birth_death/over2022
class birthdeath:
    def __init__(self, mark):
        self.config = '.\\config\\birth_death\\'.join(str(mark))
        pass

    def get_data(self, year):
        try:
            with open( self.config.join( str(year) + '.csv'), encoding='utf-8') as f:
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
            

            datalist = [birth_death_data, age_data]
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
            return datalist
            #return str(layout)

            
        except(FileNotFoundError):
            sys.stderr.write("get_data: ")


    def get_plot(self):
        plot = self.plot
        return plot
    
    def get_config(self):
        return self.config

    def get_str(self):
        return '1'
    
    #테스트용
    def test_open(self):
        try:
            with open( os.path.join(os.getcwd(),  self.config)  + '2013' +'.csv', encoding='utf-8') as f:
                test = f.read()    
            
        except FileNotFoundError:
            print("[Errno2]FILENOEFOUNDERROR")
            with open(os.path.join(os.getcwd(),  self.config) + 'test'+'.csv', 'w',encoding='utf-8') as f:
                f.write("test.csv - [Errno2] FILENOTFOUNDERROR")

        return test
    

if __name__ == '__main__':
    bd = birthdeath()
    bd.showdata()
    #bd.get_data(2013)
    