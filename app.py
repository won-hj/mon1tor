import csv
import json
import math
from bokeh.layouts import gridplot
from flask import Flask, render_template
from bokeh.embed import json_item, autoload_static, file_html, components
from bokeh.plotting import figure, show
from bokeh.resources import CDN
from flask import request
import pandas as pd
from bokeh.models import BasicTickFormatter, NumeralTickFormatter
from bokeh.models import ColumnDataSource, HoverTool, Title
from bokeh.palettes import Spectral4
import sys

from config.prediction_graph.birth_death import bdp20232027, bdp20282032
from config.prediction_graph.work_nonwork import wnwp20232027, wnwp20282032
from flask import Flask, render_template, request
from crawling import naver_crawling

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/past_graph1')
def past_graph1():
    return render_template('past_graph1.html')

@app.route('/past_graph2')
def past_graph2():
    return render_template('past_graph2.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    age = None
    if request.method == 'POST':
        age = int(request.form.get('age', None))
    elif request.method == 'GET':
        age = int(request.args.get('age', None))

    if age is None:
        return render_template('prediction.html')
    
    news_descriptions = naver_crawling.predict(age)
    return render_template('prediction.html', descriptions=news_descriptions, age=age)


if __name__ == "__main__":
    app.run()
