from helpers.date_converter import *
from helpers.countries_link_normalization import *
from model.model import *
from config import *
import urllib.request
import requests
import json

#  script variables
data_from_kiwi_url = {}
all_flights = []
sorted_data = []

#  variable needed for search in api
fly_from = 'krakow'
fly_to = ''
number_of_passengers = '2'
date_from = ''
date_to = ''
days_in_destination_from = '2'
days_in_destination_to = '4'
price_from = '0'
price_to = '60'

booking_tokens = []


def create_link(city_from, city_to, date):
    link = NODEEP + f"{city_from}/{city_to}/{date}/2-4"
    print(link)
    return link


#  in this function we do get request and
#  get all data from kiwi api
def get_data_from_kiwi_url():
    with urllib.request.urlopen(
            SEARCH_ENGINE + f"?flyFrom={fly_from}"
                            f"&to={fly_to}"
                            f"&typeFlight=return"
                            f"&daysInDestinationFrom={days_in_destination_from}"
                            f"&daysInDestinationTo={days_in_destination_to}"
                            f"&price_from={price_from}"
                            f"&price_to={price_to}"
    ) as url:
        global data_from_kiwi_url
        global all_flights
        data_from_kiwi_url = json.loads(url.read().decode())
        all_flights = data_from_kiwi_url['data']


def sort_useful_data():
    global convert_date
    for counter, key in enumerate(range(0, len(all_flights))):
        print(key)
        single_trip = {
            'cityFrom': all_flights[counter]['route'][0]['cityFrom'],
            'countryFrom': all_flights[counter]['countryFrom'],
            'cityTo': all_flights[counter]['route'][0]['cityTo'],
            'countryTo': all_flights[counter]['countryTo'],
            'date': convert_date_to_UTC(all_flights[counter]['route'][0]['dTime']),
            'return_cityFrom': all_flights[counter]['route'][1]['cityFrom'],
            'return_cityTo': all_flights[counter]['route'][1]['cityTo'],
            'return_date': convert_date_to_UTC(all_flights[counter]['route'][1]['dTime']),
            "nightsInDestination": all_flights[counter]['nightsInDest'],
            'price': all_flights[counter]['conversion']['EUR'],
            'booking_token': all_flights[counter]['booking_token'],
            "link": create_link(
                all_flights[counter]['mapIdfrom'] + "-" + normalise(all_flights[counter]['countryFrom']['name']),
                all_flights[counter]['mapIdto'] + "-" + normalise(all_flights[counter]['countryTo']['name']),
                convert_date_to_UTC(all_flights[counter]['route'][0]['dTime']))
        }
        booking_tokens.append(all_flights[counter]['booking_token'])
        sorted_data.append(single_trip)


def check_flights(booking_token):
    """
    Confirms the price of the flights, has to return true, otherwise the save_booking wont pass
    """
    parameters = {'v': 2,  # default
                  'pnum': 1,  # passenger number
                  'bnum': 0,  # number of bags
                  'booking_token': booking_token
                  }
    response = requests.get(CHECK_FLIGHTS_ENGINE, params=parameters).json()
    print(response)
    checked = response['flights_checked']
    invalid = response['flights_invalid']
    return checked, invalid


def get_data_by_default_parameters():
    get_data_from_kiwi_url()
    sort_useful_data()
    print(sorted_data)
    check_flights(booking_tokens[0])
    db.child("tripsletter").push(sorted_data)
    return unpack_data(sorted_data)


def init_search_parameters(city_from="krakow", city_to="", date_f="", date_t="", passengers="2",
                           days_in_destination_f='2',
                           days_in_destination_t='4', price_t='60'):
    global fly_from, fly_to, number_of_passengers
    global date_from, date_to
    global days_in_destination_from, days_in_destination_to, price_to
    fly_from = city_from
    fly_to = city_to
    number_of_passengers = passengers
    date_from = date_f
    date_to = date_t
    days_in_destination_from = days_in_destination_f
    days_in_destination_to = days_in_destination_t
    price_to = price_t
    get_data_from_kiwi_url()
    sort_useful_data()
    print(sorted_data)
    check_flights(booking_tokens[0])
    db.child("users_search").push(sorted_data)


def get_data_from_db():
    all_searches = db.child("users_search").get()
    for user in all_searches.each():
        print(user.val())


def unpack_data(arg):
    # global sorted_data

    data_for_telegram = ""
    for count, trip in enumerate(range(39,len(sorted_data))):
        data_for_telegram += f''' <a href="{sorted_data[count]['link']}">{sorted_data[count]['cityFrom']} - {sorted_data[count]['cityTo']}</a>   ''' \
                             f''' Price: {sorted_data[count]['price']} \n''' \
                             f'''{sorted_data[count]['date']} -  {sorted_data[count]['return_date']}  \n'''

    return data_for_telegram


# get_data_by_default_parameters()
# init_search_parameters('kiev')

get_data_from_db()
