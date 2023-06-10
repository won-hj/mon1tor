import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot, layout
import os

def create_plot(source, column, title, color): #return girdplot 이전의 각각의 plot 
    p = figure(x_range=source.data['Year'], title=title, height=400, width=400, tools="")
    p.title.align = 'center' 
    p.title.text_font = 'Consolas'
    p.title.text_font_size = '15pt'
    p.line(x='Year', y=column, line_width=5, color=color, source=source)
    p.add_tools(HoverTool(tooltips=[("Year", "@Year"), (title, "@"+column)]))
    return p

def create_graph(df, columns_titles_colors, description): #girdplot 구성과 그래프 설명
    source = ColumnDataSource(df)
    plots = [create_plot(source, column, title, color) for column, title, color in columns_titles_colors]
    grid = gridplot([plots])
<<<<<<< HEAD
    desc_div = Div(text=description, width=800, height=100, style={"font-family": "Consolas", "font-size": "16px"})
=======
    desc_div = Div(text=description, width=800, height=100, style = {"font-family": "Consolas", "font-size": "16px"})
>>>>>>> 5ebea2217fd3b0ea07b6b24c8e5c881237125803
    l = layout([
        [grid],
        [desc_div]
    ])
<<<<<<< HEAD
    return l 



current_dir = os.path.dirname(os.path.abspath(__file__))
data_file = os.path.join(current_dir, '../tool/work&nonwork_data/2013-2022data.csv')

df = pd.read_csv(data_file)
df['Year'] = df['Year'].astype(str) 

columns_titles_colors = [
    ('work_percent', '생산인구(%):15-64세', Spectral4[1]),
    ('nonwork_percent', '고령인구(%):65세 이상', Spectral4[2]),
]

description = '*대한민국 전체 인구가 100%라고 가정했을 때 비율<br>*지방 중소도시 : 50만 이하의 인구<br>*생산인구 1%당 약 16만명 감소 생산인구로만 구성된 약 1개 중소도시 삭제<br>*고령인구 1%당 약 73만명 증가 고령인구로만 구성된 약 1개 중소도시 생성'

create_graph(df, columns_titles_colors, description)
=======
    return l


if __name__ == "__main__":   #추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, '../tool/work&nonwork_data/2013-2022data.csv')

    df = pd.read_csv(data_file)
    df['Year'] = df['Year'].astype(str) 

    columns_titles_colors = [
        ('work_percent', '생산인구(%):15-64세', Spectral4[1]),
        ('nonwork_percent', '고령인구(%):65세 이상', Spectral4[2]),
    ]

    description = '*대한민국 전체 인구가 100%라고 가정했을 때 비율<br>*지방 중소도시 : 50만 이하의 인구<br>*생산인구 1%당 약 16만명 감소 생산인구로만 구성된 약 1개 중소도시 삭제<br>*고령인구 1%당 약 73만명 증가 고령인구로만 구성된 약 1개 중소도시 생성'

    graph = create_graph(df, columns_titles_colors, description)
   
>>>>>>> 5ebea2217fd3b0ea07b6b24c8e5c881237125803
