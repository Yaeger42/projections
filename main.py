from fastapi import FastAPI, HTTPException
from pony.orm import *
from pydantic import BaseModel

db = Database()
db.bind(provider='mysql', host='127.0.0.1', user='root', passwd='samplepassword', db='week5')

class Covid(db.Entity):
	CountryCodeId = Required(str)
	confirmed = Required(int)
	deaths = Required(int)
	creationDate = Required(str)

db.generate_mapping(create_tables=False)


app = FastAPI()
class CovidModel(BaseModel):
    CountryCodeId:str
    confirmed:int


@app.get('/')
async def root():
    return {'message': 'Covid 19 Cases Tracker with proyections'}


@app.get('/deaths/{country_code}/{date}')
@db_session
def get_one_country(country_code: str, date: str):
    response = {}
    query = Covid.select(lambda c: c.CountryCodeId == country_code and c.creationDate == date)
    if not query:
        raise HTTPException(status_code=404, detail="The country code and/or date didn't return any results")
    for i in query:
        print(i.CountryCodeId)
        response['CountryCodeId'] = i.CountryCodeId
        response['Confirmed'] = i.confirmed
        response['Deaths'] = i.deaths
        response['Date'] = i.creationDate
    return response
    