import pandas as pd
from pandas.core.algorithms import unique
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.ForecasterCustom import ForecasterCustom
from skforecast.ForecasterAutoregMultiOutput import ForecasterAutoregMultiOutput
from skforecast.model_selection import grid_search_forecaster
from skforecast.model_selection import time_series_spliter
from skforecast.model_selection import cv_forecaster
from skforecast.model_selection import backtesting_forecaster_intervals

warnings.filterwarnings('ignore')

# data = pd.read_csv('DeathsPerCountry.csv')


# array_of_countries = []
# for i in data['Name'].unique()[...]:
#     data_per_country = data.loc[data['Name'] == i]
#     array_of_countries.append(data_per_country)

# for df in array_of_countries:
#     print(df.iloc[[-1]])


def predictions_data_model(countryName: str = None, days: int = 90, ):
    df = pd.read_csv(countryName+'.csv', sep=',')
    if not df:
        return {"message": "The provided country was not found"}
    df['CreationDate'] = pd.to_datetime(data['CreationDate'], format='%Y/%m/%d')
    df = df.set_index('CreationDate')
    df = df.drop('Name', axis=1)
    #data = data.rename(columns={'x': 'y'})
    #print(data['CreationDate'])
    df = df.asfreq('D')
    df = df.sort_index()
    if days != 90 or days != 180 or days != 270:
        return {"message": "The number of days should be equal to 90, 180 or 270 days"}
    df_train = df[:-days]
    df_test = df[-days:]
    forecaster_rf = ForecasterAutoreg(regressor=RandomForestRegressor(random_state=123), lags=6)
    forecaster_rf.fit(y=df_train.values.flatten())
    steps_rf = days
    predictions = forecaster_rf.predict(steps=steps_rf)
    predictions = pd.Series(data=predictions, index=df_test.index)
    return predictions.to_json(orient='table', indent=4)


data = pd.read_csv('Afghanistan.csv', sep = ',')
#print(data)
data['CreationDate'] = pd.to_datetime(data['CreationDate'], format='%Y/%m/%d')
data = data.set_index('CreationDate')
data = data.drop('Name', axis=1)
#data = data.rename(columns={'x': 'y'})
#print(data['CreationDate'])
data = data.asfreq('D')
data = data.sort_index()
steps = 90
data_train = data[:-steps]
data_test = data[-steps:]
fig, ax=plt.subplots(figsize=(9, 4))
data_train.plot(ax=ax, label='train')
data_test.plot(ax=ax, label='test')
ax.legend()

forecaster_rf = ForecasterAutoreg(regressor=RandomForestRegressor(random_state=123), lags=6)
#nd_array = data_train.to_numpy()
forecaster_rf.fit(y=data_train.values.flatten())

steps_rf = 90
predictions = forecaster_rf.predict(steps=steps_rf)
predictions = pd.Series(data=predictions, index=data_test.index)

fig, ax = plt.subplots(figsize=(9,4))
data_train.plot(ax=ax, label='Train')
data_test.plot(ax=ax,label='Test')
predictions.plot(ax=ax, label='predictions')
print(data_test.to_json(orient='table', indent=4))
print(data_test.to_json(orient='table', indent=4))
print(predictions.to_json(orient='table', indent=4))
#fig.show()