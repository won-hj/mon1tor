import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.palettes import Spectral4
from bokeh.layouts import gridplot, layout

def create_plot(source, column, title, color): #return girdplot 이전의 각각의 plot 
    p = figure(x_range=source.data['Year'], title=title, height=400, width=400, tools="")
    p.line(x='Year', y=column, line_width=5, color=color, source=source)
    p.add_tools(HoverTool(tooltips=[("Year", "@Year"), (title, "@"+column)]))
    return p

def create_graph(df, columns_titles_colors): #girdplot 구성
    source = ColumnDataSource(df)
    plots = [create_plot(source, column, title, color) for column, title, color in columns_titles_colors]
    grid = gridplot([plots])
    
df = pd.read_csv('../tool/work&nonwork_data/-2022_data.csv')
df['Year'] = df['Year'].astype(str) 

columns_titles_colors = [
    ('work_percent', '생산인구(%):15-64세', Spectral4[1]),
    ('nonwork_percent', '고령인구(%):65세 이상', Spectral4[2]),
]

create_graph(df, columns_titles_colors)