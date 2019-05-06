import requests
import datetime
import plotly.plotly as py
import plotly.graph_objs as go
from plotly import tools
from dotenv import load_dotenv
from os import getenv


def get_timestamp(day):
    return datetime.datetime(day.year, day.month, day.day, 0, 0, 0).timestamp()


def get_day_before_today(number_of_day):
    beginning_of_target_day = datetime.date.today() - datetime.timedelta(days=number_of_day)
    end_of_target_day = datetime.date.today() - datetime.timedelta(days=number_of_day - 1)
    return beginning_of_target_day, get_timestamp(beginning_of_target_day), get_timestamp(end_of_target_day)


def get_amount_of_mentions(number_of_day):
    service_key = getenv("SERVICE_KEY")
    response = requests.get('https://api.vk.com/method/newsfeed.search', params={
    'v': 5.95,
    'access_token': service_key,
    'q': 'Coca-Cola',
    'start_time': get_day_before_today(number_of_day)[1],
    'end_time': get_day_before_today(number_of_day)[2]
    })
    return response.json()['response']['total_count']


if __name__ == '__main__':
    days = [get_amount_of_mentions(day) for day in range(1, 8)]
    load_dotenv()
    tools.set_credentials_file(username=getenv('USERNAME'), api_key=getenv('API_KEY'))
    scatter = go.Scatter(list(range(1, 8)), days)
    print(py.plot(scatter, filename='basic-line', auto_open=False))
