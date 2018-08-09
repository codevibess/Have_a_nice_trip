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
fly_to = 'berlin'
number_of_passengers = '2'
date_from = '08/08/2018'
date_to = '08/12/2018'
days_in_destination_from = '2'
days_in_destination_to = '4'
price_from = '0'
price_to = '52'


booking_tokens = []


def create_link(city_from, city_to, date):
    link = NODEEP + f"{city_from}/{city_to}/{date}/2-4"
    return link


#  in this function we do get request and
#  get all data from kiwi api
def get_data_from_kiwi_url():
    with urllib.request.urlopen(

            # SEARCH_ENGINE + f"?flyFrom={fly_from}"
            #                 f"&to={fly_to}"
            #                 f"&typeFlight=return"
            #                 f"&daysInDestinationFrom={days_in_destination_from}"
            #                 f"&daysInDestinationTo={days_in_destination_to}"
            #                 f"&price_from={price_from}"
            #                 f"&price_to={price_to}"
            #                 f"&dateFrom={date_from}"
            #                 f"&dateTo={date_to}"
         SEARCH_ENGINE + f"?flyFrom={fly_from}"
                         f"&to={fly_to}"
                         f"&typeFlight=return"
                         f"&daysInDestinationFrom={days_in_destination_from}"
                         f"&daysInDestinationTo={days_in_destination_to}"
                         f"&price_from={price_from}"
                         f"&price_to={price_to}&"
                         f"dateFrom={date_from}"
                         f"&dateTo={date_to}"


    ) as url:
        print(

            SEARCH_ENGINE + f"?flyFrom={fly_from}"
                            f"&to={fly_to}"
                            f"&typeFlight=return"
                            f"&daysInDestinationFrom={days_in_destination_from}"
                            f"&daysInDestinationTo={days_in_destination_to}"
                            f"&price_from={price_from}"
                            f"&price_to={price_to}"
                            f"&dateFrom={date_from}"
                            f"&dateTo={date_to}"

                              )

        global data_from_kiwi_url
        global all_flights
        data_from_kiwi_url = json.loads(url.read().decode())
        all_flights = data_from_kiwi_url['data']


def sort_useful_data():
    global convert_date
    for counter, key in enumerate(range(0, len(all_flights))):
        single_trip = {
            'cityFrom': all_flights[counter]['mapIdfrom'],
            'countryFrom': all_flights[counter]['countryFrom'],
            'cityTo': all_flights[counter]['mapIdto'],
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
                convert_date_to_UTC(all_flights[counter]['route'][0]['dTime'])),
            "cityFromFullName": all_flights[counter]['cityFrom'],
            "cityToFullName": all_flights[counter]['cityTo']
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

    print(check_flights(booking_tokens[0]))
    db.child("tripsletter").push(sorted_data)
    return unpack_data()


def init_search_parameters(city_from="krakow", city_to="", date_f="08/08/2018", date_t="20/12/2018", passengers="1",
                           days_in_destination_f='2',
                           days_in_destination_t='4', price_t='60'):
    ''' Function which init global parameters for user search '''
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
    # print(sorted_data)
    # call check flights for more information about single flight ex. number of seats, bags fee
    print(check_flights(booking_tokens[0]))
    # put into firebase data
    db.child("users_search").push(sorted_data)
    return unpack_data()


def get_data_from_db():
    all_searches = db.child("users_search").get()
    result = []
    for user in all_searches.each():
        result.append(user.val())
    return result


def unpack_data():
    global sorted_data

    list_of_flights = []
    for count, trip in enumerate(sorted_data):
        data_for_telegram = f''' <a href="{sorted_data[count]['link']}">{sorted_data[count]['cityFromFullName']} - {sorted_data[count]['cityToFullName']}</a>''' \
                            f''' Price: <b>{sorted_data[count]['price']}</b> \n''' \
                            f'''{sorted_data[count]['date']} -  {sorted_data[count]['return_date']}  \n'''
        list_of_flights.append(data_for_telegram)
    # print(list_of_flights)
    sorted_data.clear()
    return list_of_flights



