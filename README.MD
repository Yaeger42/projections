# How to run the project locally
## Requirements
Given the fact that this project relies on a mySQL database you are going to need one, either via docker or an actual instance.
- MySQL Database
- Virtual environment (unless you don't mind clouding up your python installation)

## Initial steps

Once you have a connection to the MySQL db that you're going to use, use your prefered console and run the scripts inside the dbscripts folder in this order:
1. ```Initial.sql```
2. ```insertionsCountriesCodes.sql```
3. ```InsertionCountriesNames.sql```

Once that's done activate your python virtual environment and run (you may skip this if you don't use a virtual environment):
```(env)$ pip install -r requirements.txt```

### Upload the data

On the root folder run the ```etl.py``` with ```(env)$ python3 etl.py``` and wait for it to finish

### Run the FastAPI server
On the root folder run: ```(env)$ uvicorn main:app --reload``` 

### Querying the API
-- TODO