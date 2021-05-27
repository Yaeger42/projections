from pony.orm import *
import requests

request = requests.get('https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/2019-01-01/2021-05-26')
data = request.json()

# Database connection
db = Database()
db.bind(provider='mysql', host='127.0.0.1', user='root', passwd='samplepassword', db='week5')

# Making the main entity to be able to insert into week5.covid
class Covid(db.Entity):
	CountryCodeId = Required(str)
	confirmed = Required(int)
	deaths = Required(int)
	creationDate = Required(str)

# Create tables set to false because no table creation is needed, the schema is built already
db.generate_mapping(create_tables=False)

@db_session
def insert_data(data):
	for date, v in data['data'].items():
		for key, value in v.items():
			if value['deaths'] is None:
				continue
			c = Covid(CountryCodeId = key, confirmed=value['confirmed'], deaths=value['deaths'], creationDate=value['date_value'])

# Main runner
insert_data(data)