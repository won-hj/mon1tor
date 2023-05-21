import pandas as pd
from prophet import Prophet

def load_original_data(file_path): #return 기존 csv 경로
    return pd.read_csv(file_path)

def fit_prophet_model(data):    #return prophet 예측 model
    model = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)
    model.fit(data)
    return model

def predict_future_data(model, future_dates): #return 5개년에 대한 예측 value
    forecast = model.predict(pd.DataFrame({'ds': future_dates}))
    return forecast['yhat'].astype(int)

def create_yearly_data(start_year, end_year): #return df with columns
    years = range(start_year, end_year + 1)
    data = pd.DataFrame({'Year': years, 'Birth': [0] * len(years), 'Death': [0] * len(years)})
    return data

start_year = 2023
end_year = 2027

predicted_data = load_original_data('./tool/first_data.csv')

m_births = fit_prophet_model(predicted_data[['year', 'births']].rename(columns={'year': 'ds', 'births': 'y'}))
m_deaths = fit_prophet_model(predicted_data[['year', 'deaths']].rename(columns={'year': 'ds', 'deaths': 'y'}))

future_dates = pd.date_range(start=str(start_year - 1), end=str(end_year + 1), freq='Y')

forecast_births = predict_future_data(m_births, future_dates)
forecast_deaths = predict_future_data(m_deaths, future_dates)

data = create_yearly_data(start_year, end_year)