import pandas as pd
from prophet import Prophet
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.formatters import NumeralTickFormatter, DatetimeTickFormatter
from bokeh.models import HoverTool, Title


class ForecastPlotter:
    def __init__(self, data, target_columns, title):
        self.data = data
        self.target_columns = target_columns
        self.title = title

    def preprocess_data(self):#bokeh 사용을 위해 datetime형식으로 변환
        self.data['year'] = pd.to_datetime(self.data['year'], format='%Y')

    def fit_models(self): #prophet예측
        m_births = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)
        m_deaths = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)

        births_data = self.data[['year', self.target_columns[0]]].rename(columns={'year': 'ds', self.target_columns[0]: 'y'})
        deaths_data = self.data[['year', self.target_columns[1]]].rename(columns={'year': 'ds', self.target_columns[1]: 'y'})

        m_births.fit(births_data)
        m_deaths.fit(deaths_data)

        future_start_date = pd.to_datetime('2022')
        future_end_date = pd.to_datetime('2027')

        future_dates = pd.date_range(start=future_start_date, end=future_end_date, freq='Y')

        self.forecast_births = m_births.predict(pd.DataFrame({'ds': future_dates}))
        self.forecast_deaths = m_deaths.predict(pd.DataFrame({'ds': future_dates}))

    def plot(self):#bokeh시각화
        self.preprocess_data()
        self.fit_models()

        p = figure(title=Title(text=self.title, align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"),
                    x_axis_type='datetime', width=1200, height=500)

        
        p.xaxis.formatter = DatetimeTickFormatter(years='%Y')
        
        births_hover_tool = HoverTool(tooltips=[("출생아 수", "@y{0,0}")], formatters={"@x": "datetime"})
        deaths_hover_tool = HoverTool(tooltips=[("사망자 수", "@y{0,0}")], formatters={"@x": "datetime"})

        p.add_tools(births_hover_tool)
        p.add_tools(deaths_hover_tool)

        source_births = ColumnDataSource(data=dict(
            x=self.forecast_births['ds'],
            y=self.forecast_births['yhat'],
            y_upper=self.forecast_births['yhat_upper'],
            y_lower=self.forecast_births['yhat_lower']
        ))

        source_deaths = ColumnDataSource(data=dict(
            x=self.forecast_deaths['ds'],
            y=self.forecast_deaths['yhat'],
            y_upper=self.forecast_deaths['yhat_upper'],
            y_lower=self.forecast_deaths['yhat_lower']
        ))

        p.line(x='x', y='y', source=source_births, color='red', legend_label='출생아 수')
        p.varea(x='x', y1='y_lower', y2='y_upper', source=source_births, color='red', alpha=0.1)
        p.line(x='x', y='y', source=source_deaths, color='blue', legend_label='사망자 수')
        p.varea(x='x', y1='y_lower', y2='y_upper', source=source_deaths, color='blue', alpha=0.1)

        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"

        show(p)

data = pd.read_csv('./first_data.csv')

forecast_plotter = ForecastPlotter(data, ['births', 'deaths'], '2023-2027')
forecast_plotter.plot()