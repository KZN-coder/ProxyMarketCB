import kaleido
import plotly.graph_objects as go
import requests
import config
from datetime import datetime

API_KEY = f'{config.proxy_API_KEY}'

get_proxy_data = {
    "page": '1',
    "perPage": '20',
}

def get_data():
    response = requests.get(f'https://api.dashboard.proxy.market/dev-api/v2/packages/{API_KEY}', json=get_proxy_data)
    responce_data = response.json()
    print("Recieved new data")
    print(response.status_code)
    return responce_data

def get_proxy_lists(id):
    get_proxy_lists_data = {
        "type": "all",
        "proxy_type": "resident",
        "page": 1,
        "page_size": 20,
        "sort": 0,
        "package_id": id
    }
    response = requests.post(f'https://api.dashboard.proxy.market/dev-api/list/{API_KEY}', json=get_proxy_lists_data)
    response_data = response.json()
    print("Recieved lists")
    print(response.status_code)
    return response_data

def formating_proxy_lists(id):
    data = get_proxy_lists(id)["list"]["data"]
    output = ""
    for item in data:
        output+= f'{item["login"]}:{item["password"]}@{item["ip"]}:10000' + ','
    return output

def get_image():
    data = get_data()
    names = []
    remaining = []
    for item in data["data"]:
        used = round(((int(item["used"])) / (1024 * 1024)), 2)
        total = round((int(item["total"])) / (1024 * 1024), 2)
        lasts = round(total - used, 2)
        if lasts > 0:
            names.append(item["name"] + ' (' + str(item["id"]) + ')')
            remaining.append(lasts)
    # Создание диаграммы
    fig = go.Figure(go.Bar(
        y=remaining,
        x=names,
        orientation='v',
        marker=dict(color='#dbc360'),
        text=remaining,  # Добавление текста на столбцы
        textposition='inside',  # Позиция текста внутри столбцов
        textfont=dict(color='black', size=20)  # Настройка шрифта
    ))

    fig.update_layout(
        xaxis_title='Название списка',
        yaxis_title='Оставшийся трафик (Mb)',
        font=dict(color='black', size=20),
        width=1920,  # Ширина изображения
        height=1080  # Высота изображения
    )
    fig.write_image("./data/proxy_traffic.png", scale=3)

def get_list():
    output = "Available proxy list: \n\n-----\n\n"
    data = get_data()
    for item in data["data"]:
        used = round(((int(item["used"])) / (1024 * 1024)), 2)
        total = round((int(item["total"])) / (1024 * 1024), 2)
        lasts = round(total - used, 2)
        if lasts > 0:
            output += "List: *" + item["name"] + "*" + '\n'
            output += "Lasts: _" + str(lasts) + "Mb_" + '\n'
            output += "Used: _" + str(used) + "Mb_" + " from _" + str(total) + "Mb_ \n"
            output += "Expires at: " + convert_timestamp_to_date(int(item["expires_at"])) + '\n\n-----\n\n'
    return output


def convert_timestamp_to_date(timestamp):
    date_object = datetime.fromtimestamp(timestamp)
    formatted_date = date_object.strftime('%d %B %H:%M:%S')
    return formatted_date