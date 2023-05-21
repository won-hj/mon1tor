import pandas as pd
from prophet import Prophet

def load_original_data(file_path): #return 기존 csv 경로
    return pd.read_csv(file_path)

def fit_prophet_model(data):    #5개년 예측 return 예측model
    model = Prophet(changepoint_prior_scale=0.001, seasonality_mode='multiplicative', yearly_seasonality=5)
    model.fit(data)
    return model

predicted_data = load_original_data('./tool/first_data.csv')

m_births = fit_prophet_model(predicted_data[['year', 'births']].rename(columns={'year': 'ds', 'births': 'y'}))
m_deaths = fit_prophet_model(predicted_data[['year', 'deaths']].rename(columns={'year': 'ds', 'deaths': 'y'}))