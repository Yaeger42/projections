import requests


def test_root_returns_200():
    response = requests.get('http://localhost:8000')
    assert response.status_code == 200

def test_api_returns_contentType_json():
    response = requests.get('http://localhost:8000')
    assert response.headers['content-type'] == 'application/json'

def test_api_has_confirmed_in_body():
    response = requests.get('http://localhost:8000/deaths/USA/2021-05-20').json()
    assert 'Confirmed' in response.keys()

def test_api_has_deaths_in_body():
    response = requests.get('http://localhost:8000/deaths/USA/2021-05-20').json()
    assert 'Deaths' in response.keys()

def test_api_returns_correct_country():
    country = 'USA'
    response = requests.get(f'http://localhost:8000/deaths/{country}/2021-05-20').json()
    assert 'USA' == response['CountryCodeId']

def test_api_has_code_id_in_response():
    response = requests.get('http://localhost:8000/deaths/USA/2021-05-20').json()
    assert 'CountryCodeId' in response.keys()

def test_api_returns_404_when_querying_for_wrong_date():
    response = requests.get('http://localhost:8000/deaths/USA/2021-05-29')
    assert response.status_code == 404

def test_api_returns_404_when_querying_wrong_country():
    response = requests.get('http://localhost:8000/deaths/CIB/2021-05-21')
    assert response.status_code == 404