import pandas as pd
from prophet import Prophet
import os

def load_original_data(file_path): #return 기존 csv 경로
    return pd.read_csv(file_path)

def fit_prophet_model(data):    #return prophet 예측 model
    model = Prophet(changepoint_prior_scale=0.0001, seasonality_mode='multiplicative', yearly_seasonality=1)
    model.fit(data)
    return model

def predict_birth_future_data(model, future_dates): #return 5개년에 대한 예측 upper_value
    forecast = model.predict(pd.DataFrame({'ds': future_dates}))
    return forecast['yhat_upper'].astype(int)

def predict_death_future_data(model, future_dates): #return 5개년에 대한 예측 value
    forecast = model.predict(pd.DataFrame({'ds': future_dates}))
    return forecast['yhat'].astype(int)

def create_yearly_data(start_year, end_year): #return df with columns
    years = range(start_year, end_year + 1)
    data = pd.DataFrame({'year': years, 'births': [0] * len(years), 'deaths': [0] * len(years)})
    return data

def fill_predicted_data(data, years, births, deaths): #return 데이터프레임을 위한 columndata들
    data.loc[data['year'].isin(years), 'births'] = births
    data.loc[data['year'].isin(years), 'deaths'] = deaths
    return data

def extract_data_to_csv(data, file_path): #데이터프레임을 csv로 추출
    data.to_csv(file_path, index=False)

def combine_data(first_data_path, new_data_path, combined_data_path): #추출한 data와 병합 
    first_data = pd.read_csv(first_data_path)
    new_data = pd.read_csv(new_data_path)
    combined_data = pd.concat([first_data, new_data], ignore_index=True)
    combined_data.to_csv(combined_data_path, index=False)

start_year = 2032
end_year = 2036

predicted_data = load_original_data('../tool/birth&death_data/-2032data.csv')

m_births = fit_prophet_model(predicted_data[['year', 'births']].rename(columns={'year': 'ds', 'births': 'y'}))
m_deaths = fit_prophet_model(predicted_data[['year', 'deaths']].rename(columns={'year': 'ds', 'deaths': 'y'}))

future_dates = pd.date_range(start=str(start_year - 1), end=str(end_year + 1), freq='Y')

forecast_births = predict_birth_future_data(m_births, future_dates)
forecast_deaths = predict_death_future_data(m_deaths, future_dates)

data = create_yearly_data(start_year, end_year)
data = fill_predicted_data(data, range(start_year, end_year + 1), forecast_births, forecast_deaths)

extract_data_to_csv(data, '../tool/birth&death_data/tempdata.csv')

first_data = pd.read_csv('../tool/birth&death_data/-2032data.csv')
new_data = pd.read_csv('../tool/birth&death_data/tempdata.csv')

combine_data('../tool/birth&death_data/-2032data.csv', '../tool/birth&death_data/tempdata.csv', '../tool/birth&death_data/-2036data.csv')

os.remove('../tool/birth&death_data/tempdata.csv')