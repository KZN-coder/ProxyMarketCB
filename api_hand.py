import requests

API_KEY = ''
url = f'https://api.dashboard.proxy.market/dev-api/v2/packages/{API_KEY}'

data = {
    "page": '1',
    "perPage": '20',
}

def get_data():
    response = requests.get(url, json=data)
    responce_data = response.json()
    return responce_data