import pyrebase
from config import *

config = {
    "apiKey": API_KEY,
    "authDomain": AUTH_DOMAIN,
    "databaseURL": DATABASE_URL,
    "storageBucket": STORE_BUCKET
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
