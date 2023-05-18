import pandas as pd
from prophet import Prophet
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.formatters import NumeralTickFormatter, DatetimeTickFormatter
from bokeh.models import ColumnDataSource, HoverTool, Title

data = pd.read_csv('./first_data.csv')

data['year'] = pd.to_datetime(data['year'], format='%Y')
births_data = data[['year', 'births']].rename(columns={'year': 'ds', 'births': 'y'})
deaths_data = data[['year', 'deaths']].rename(columns={'year': 'ds', 'deaths': 'y'})

m_births = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)
m_deaths = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)

m_births.fit(births_data)
m_deaths.fit(deaths_data)

future_births = m_births.make_future_dataframe(periods=5, freq='Y')
future_deaths = m_deaths.make_future_dataframe(periods=5, freq='Y')

forecast_births = m_births.predict(future_births)
forecast_deaths = m_deaths.predict(future_deaths)

p = figure(title='Prediction Graph', x_axis_label='Year', y_axis_label='Births/Deaths', x_axis_type='datetime', width=1200, height=500)

p.xaxis[0].ticker.desired_num_ticks = len(forecast_births) + 1
p.xaxis[0].ticker.num_minor_ticks = 0
p.xaxis.formatter = DatetimeTickFormatter(years='%Y')

source_births = ColumnDataSource(data=dict(
    x=forecast_births['ds'],
    y=forecast_births['yhat'],
    y_upper=forecast_births['yhat_upper'],
    y_lower=forecast_births['yhat_lower']
))

source_deaths = ColumnDataSource(data=dict(
    x=forecast_deaths['ds'],
    y=forecast_deaths['yhat'],
    y_upper=forecast_deaths['yhat_upper'],
    y_lower=forecast_deaths['yhat_lower']
))

p.line(x='x', y='y', source=source_births, color='red', legend_label='Births')
p.varea(x='x', y1='y_lower', y2='y_upper', source=source_births, color='red', alpha=0.1)
p.line(x='x', y='y', source=source_deaths, color='blue', legend_label='Deaths')
p.varea(x='x', y1='y_lower', y2='y_upper', source=source_deaths, color='blue', alpha=0.1)

p.yaxis.formatter = NumeralTickFormatter(format="0,0")

hover_tool = HoverTool(tooltips=[("Year", "@x{%Y}"), ("Number of births", "@y{0,0}")], formatters={"@x": "datetime"})
p.add_tools(hover_tool)

show(p)