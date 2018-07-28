from config import *
import urllib.request
import requests
import json
import datetime

#  script variables
data_from_kiwi_url = {}
all_flights = []
sorted_data = []

#  variable needed for search in api
fly_from = 'kiev'
fly_to = ''
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


#  this function convert date form UNIX format to UTC
def convert_date_to_UTC(date):
    return datetime.datetime.fromtimestamp(
        int(date)
    ).strftime('%Y-%m-%d')


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
        print(SEARCH_ENGINE + f"?flyFrom={fly_from}"
                            f"&to={fly_to}"
                            f"&typeFlight=return"
                            f"&daysInDestinationFrom={days_in_destination_from}"
                            f"&daysInDestinationTo={days_in_destination_to}"
                            f"&price_from={price_from}"
                            f"&price_to={price_to}")
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
                all_flights[counter]['mapIdfrom'] + "-" + all_flights[counter]['countryFrom']['name'].lower().replace(
                    " ", "-"),
                all_flights[counter]['mapIdto'] + "-" + all_flights[counter]['countryTo']['name'].lower().replace(" ",
                                                                                                                  "-"),
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
# www.kiwi.com/deep?flyFrom=krakow&price_from=0&price_to=60&typeFlight=return&daysInDestinationFrom=2&daysInDestinationTo=4
# www.kiwi.com/deep?departure=2018-10-24&return=2-4&from=KRK&to=GDN&partner=picky
get_data_by_default_parameters()