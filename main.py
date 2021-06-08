from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pony.orm import *
from pydantic import BaseModel
import os
import pandas as pd
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.linear_model import Lasso


db = Database()
db.bind(provider='mysql', host=os.environ['mysqlhost'], user=os.environ['mysqluser'],
passwd=os.environ['mysqlpassword'], db=os.environ['mysqldatabase'])


class Covid(db.Entity):
	CountryCodeId = Required(str)
	confirmed = Required(int)
	deaths = Required(int)
	creationDate = Required(str)


class CountriesNames(db.Entity):
	Name = Required(str)
	CountryCodeId = Required(str)


db.generate_mapping(create_tables=False)


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['GET'],
    allow_headers=['*']
)

class CovidModel(BaseModel):
    CountryCodeId: str
    confirmed: int


@app.get('/')
async def root():
    return {'message': 'Covid 19 Cases Tracker with proyections'}


@app.get('/deaths/{country_code}/{date}')
@db_session
def get_one_country(country_code: str, date: str):
    response = {}
    query = Covid.select(lambda c: c.CountryCodeId ==
                         country_code and c.creationDate == date)
    if not query:
        raise HTTPException(
            status_code=404, detail="The country code and/or date didn't return any results")
    for i in query:
        print(i.CountryCodeId)
        response['CountryCodeId'] = i.CountryCodeId
        response['Confirmed'] = i.confirmed
        response['Deaths'] = i.deaths
        response['Date'] = i.creationDate
    return response



@app.get('/getAllCountries')
@db_session
def get_countries():
    query = select(c for c in CountriesNames)
    json_response = []
    for i in query:
        obj = {}
        obj['CountryName'] = i.Name
        obj['CountryCodeId'] = i.CountryCodeId
        json_response.append(obj)
    return json_response


@app.get('/getCountryCode/{country_name}')
@db_session
def get_country_code(country_name: str):
    query = CountriesNames.select(lambda c: c.Name == country_name)
    if not query:
        raise HTTPException(status_code=404, detail="The country code and/or date didn't return any results")
    response = {}
    for i in query:
        response['CountryCode'] = i.CountryCodeId
        response['CountryName'] = i.Name
    return response

# 
@app.get('/getMaxDeathsPercountry/{country_code}')
@db_session
def get_countries(country_code: str):
    country_code.upper()
    q = db.select("""SELECT
    MAX(c.creationDate),
    cN.Name,
    MAX(c.Deaths)
	FROM
    covid c
	JOIN countriesnames cN on c.CountryCodeId = cN.CountryCodeId
	WHERE cN.CountryCodeId = $country_code;""")
    if q is None:
       raise HTTPException(status_code=404, detail="The country code and/or date didn't return any results")
     
    response_object = {}
    for date, country, deaths in q:
	    response_object['Country'] = country
	    response_object['Deaths'] = deaths
	    response_object['Date'] = date

    return response_object

# Change dates
@app.get('/getDeathsRatioPerCountry/{country_code}')
@db_session
def get_death_ratio(country_code: str):
    country_code.upper()
    q = db.select("""SELECT
    MAX(c.creationDate),
    cn.Name,
    Max(c.Deaths),
    p.TotalPopulation,
    Max(c.Deaths) / 100000 'Ratio_per_100_000',
    ROUND((MAX(c.Deaths) / p.TotalPopulation) * 100, 5) 'Total_Ratio'
    FROM
    covid c
    JOIN countriesnames cn on c.CountryCodeId = cn.CountryCodeId
    JOIN population p on c.CountryCodeId = p.CountryCodeId  AND c.CountryCodeId = $country_code;
    """)

    if q is None:
        raise HTTPException(status_code=404, detail="The country code and/or date didn't return any results")

    response_object = {}
    for date, country, deaths, totalPopulation, ratio_per_100_000, total_ratio in q:
        response_object['Country'] = country
        response_object['Deaths'] = deaths
        response_object['Population'] = totalPopulation
        response_object['RatioPer100K'] = ratio_per_100_000
        response_object['TotalRatio'] = total_ratio
        response_object['Date'] = date

    return response_object

@app.get('/getPredictions/{country_name}/{month_in_days}')
def predictions_data_model(country_name: str = None, days: int = 90, ):
    dir_path = os.path.dirname(os.path.realpath(__file__)) 
    df = pd.read_csv(f'{dir_path}/data/{country_name.capitalize()}.csv', sep=',')
    if df.empty:
        return {"message": "The provided country was not found"}
    df['CreationDate'] = pd.to_datetime(df['CreationDate'], format='%Y/%m/%d')
    df = df.set_index('CreationDate')
    df = df.drop('Name', axis=1)
    df = df.asfreq('D')
    df = df.sort_index()
    if days != 90 and days != 180 and days != 270:
        return {"message": "The number of days should be equal to 90, 180 or 270 days"}
    try:
        df_train = df[:-days]
        df_test = df[-days:]
        forecaster_rf = ForecasterAutoreg(regressor=Lasso(), lags=100)
        forecaster_rf.fit(y=df_train.values.flatten())
        steps_rf = days
        predictions = forecaster_rf.predict(steps=steps_rf)
        predictions = pd.Series(data=predictions, index=df_test.index)
        return predictions.to_json(orient='table', indent=4)
    except IndexError:
        return {'message': "There is not enough data to predict that far away"}
