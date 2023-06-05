import pandas as pd
from prophet import Prophet
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, FixedTicker
from bokeh.models.formatters import NumeralTickFormatter, DatetimeTickFormatter
from bokeh.models import HoverTool, Title
from bokeh.palettes import Spectral4

class ForecastPlotter:
    def __init__(self, data, target_columns, title):
        self.data = data
        self.target_columns = target_columns
        self.title = title

    def preprocess_data(self):#bokeh 사용을 위해 datetime형식으로 변환
        self.data['Year'] = pd.to_datetime(self.data['Year'], format='%Y')

    def fit_models(self): #prophet예측
        m_work = Prophet(changepoint_prior_scale=1,seasonality_mode='multiplicative', yearly_seasonality=5)
        m_nonwork = Prophet(changepoint_prior_scale=0.01,seasonality_mode='multiplicative', yearly_seasonality=5)

        work_data = self.data[['Year', self.target_columns[0]]].rename(columns={'Year': 'ds', self.target_columns[0]: 'y'})
        nonwork_data = self.data[['Year', self.target_columns[1]]].rename(columns={'Year': 'ds', self.target_columns[1]: 'y'})

        m_work.fit(work_data)
        m_nonwork.fit(nonwork_data)

        future_start_date = pd.to_datetime('2032')
        future_end_date = pd.to_datetime('2037')

        future_dates = pd.date_range(start=future_start_date, end=future_end_date, freq='Y')

        self.forecast_work = m_work.predict(pd.DataFrame({'ds': future_dates}))
        self.forecast_nonwork = m_nonwork.predict(pd.DataFrame({'ds': future_dates}))

    def plot(self): #bokeh 시각화
        self.preprocess_data()
        self.fit_models()

        p = figure(title=Title(text=self.title, align="center", text_font_size="22px", text_font="Consolas", text_font_style="bold"),
                x_axis_type='datetime', width=800, height=400)

        p.xaxis.ticker = FixedTicker(ticks=pd.date_range(start='2013', end='2037', freq='YS').astype(int) / 10**6)
        p.xaxis.formatter = DatetimeTickFormatter(years='%Y')

        source_work = ColumnDataSource(data=dict(
            x=self.forecast_work['ds'],
            y=self.forecast_work['yhat'],
        ))

        source_nonwork = ColumnDataSource(data=dict(
            x=self.forecast_nonwork['ds'],
            y=self.forecast_nonwork['yhat'],
        ))

        work_line = p.line(x='x', y='y', source=source_work, color=Spectral4[1], legend_label='생산가능인구:15-64세(단위:천 명)',width=7)
        nonwork_line = p.line(x='x', y='y', source=source_nonwork, color=Spectral4[2], legend_label='비노동자수:65세이상(단위:천 명)',width=7)

        work_hover_tool = HoverTool(renderers=[work_line], tooltips=[("15-64세(단위:천 명)", "@y{0,0}")])
        nonwork_hover_tool = HoverTool(renderers=[nonwork_line], tooltips=[("65세이상(단위:천 명)", "@y{0,0}")])

        p.add_tools(work_hover_tool)
        p.add_tools(nonwork_hover_tool)

        p.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p.legend.location = "center_left"
        p.legend.orientation = "horizontal"

        show(p)

data = pd.read_csv('../../tool/work&nonwork_data/-2032_data.csv')

forecast_plotter = ForecastPlotter(data, ['work_demo', 'nonwork_demo'], '2033-2037 생산가능인구/생산불가능인구 변화')
forecast_plotter.plot()