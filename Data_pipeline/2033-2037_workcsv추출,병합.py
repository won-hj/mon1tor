import pandas as pd
from prophet import Prophet
import os

def load_original_data(file_path): #return 기존 csv 경로
    return pd.read_csv(file_path)

def fit_prophet_work_model(data):    #return work_demo prophet 예측 model
    model = Prophet(changepoint_prior_scale=1, seasonality_mode='multiplicative', yearly_seasonality=5)
    model.fit(data)
    return model

def fit_prophet_nonwork_model(data):    #return nonwork_demo prophet 예측 model
    model = Prophet(changepoint_prior_scale=0.01, seasonality_mode='multiplicative', yearly_seasonality=5)
    model.fit(data)
    return model

def predict_future_data(model, future_dates): #return 5개년에 대한 예측 upper_value
    forecast = model.predict(pd.DataFrame({'ds': future_dates}))
    return forecast['yhat'].astype(int)

def create_yearly_data(start_year, end_year): #return df with columns
    years = range(start_year, end_year + 1)
    data = pd.DataFrame({'Year': years, 'work_demo': [0] * len(years), 'nonwork_demo': [0] * len(years)})
    return data

def fill_predicted_data(data, years, births, deaths): #return 데이터프레임을 위한 columndata들
    data.loc[data['Year'].isin(years), 'work_demo'] = births
    data.loc[data['Year'].isin(years), 'nonwork_demo'] = deaths
    return data

def extract_data_to_csv(data, file_path): #데이터프레임을 csv로 추출
    data.to_csv(file_path, index=False)

def combine_data(first_data_path, new_data_path, combined_data_path): #추출한 data와 병합 
    first_data = pd.read_csv(first_data_path)
    new_data = pd.read_csv(new_data_path)
    combined_data = pd.concat([first_data, new_data], ignore_index=True)
    combined_data.to_csv(combined_data_path, index=False)

start_year = 2033
end_year = 2037

predicted_data = load_original_data('../tool/work&nonwork_data/-2032_data.csv')

m_works = fit_prophet_work_model(predicted_data[['Year', 'work_demo']].rename(columns={'Year': 'ds', 'work_demo': 'y'}))
m_non_works = fit_prophet_nonwork_model(predicted_data[['Year', 'nonwork_demo']].rename(columns={'Year': 'ds', 'nonwork_demo': 'y'}))

future_dates = pd.date_range(start=str(start_year - 1), end=str(end_year + 1), freq='Y')

forecast_works = predict_future_data(m_works, future_dates)
forecast_non_works = predict_future_data(m_non_works, future_dates)

data = create_yearly_data(start_year, end_year)
data = fill_predicted_data(data, range(start_year, end_year + 1), forecast_works, forecast_non_works)

extract_data_to_csv(data, '../tool/work&nonwork_data/tempdata.csv')

first_data = pd.read_csv('../tool/work&nonwork_data/-2032_data.csv')
new_data = pd.read_csv('../tool/work&nonwork_data/tempdata.csv')

combine_data('../tool/work&nonwork_data/-2032_data.csv', '../tool/work&nonwork_data/tempdata.csv', '../tool/work&nonwork_data/-2037_data.csv')

os.remove('../tool/work&nonwork_data/tempdata.csv')