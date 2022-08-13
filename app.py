
import streamlit as st
import numpy as np
import pandas as pd
import requests
import datetime
from shapely.geometry import Point, Polygon
import geopandas as gpd
import pandas as pd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

'''
# New York Taxi Fare Estimator

## Using a machine learning model
'''

date_input = st.date_input('pickup_date', value=datetime.datetime(2022, 7, 6, 11, 14, 28))
time_input = st.time_input('pickup_time', value=datetime.datetime(2022, 7, 6, 11, 14, 28))
pickup_datetime =f'{date_input} {time_input}'

street_pickup = st.sidebar.text_input("street_pickup", "4 Pennsylvania Plaza")
city_pickup = st.sidebar.text_input("city_pickup", "New York")
# province_pickup = st.sidebar.text_input("Province Pickup", "Ontario")
# country_pickup = st.sidebar.text_input("country_pickup", "United States")

street_dropoff = st.sidebar.text_input("street_dropoff", "31-10 Thomson Ave")
city_dropoff = st.sidebar.text_input("city_dropoff", "Queens")
# province_dropoff = st.sidebar.text_input("Province Dropoff", "Ontario")
# country_dropoff = st.sidebar.text_input("country_dropoff", "United States")

geolocator = Nominatim(user_agent="GTA Lookup")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
location_pickup = geolocator.geocode(street_pickup+", "+city_pickup)
location_dropoff = geolocator.geocode(street_dropoff+", "+city_dropoff)

pickup_lat = location_pickup.latitude
pickup_lon = location_pickup.longitude
dropoff_lat = location_dropoff.latitude
dropoff_lon = location_dropoff.longitude

passenger_count = st.number_input("passenger_count", 1)

url = 'https://taxifare.lewagon.ai/predict'

params = dict(
  pickup_datetime=pickup_datetime,
  pickup_longitude=pickup_lon,
  pickup_latitude=pickup_lat,
  dropoff_longitude=dropoff_lon,
  dropoff_latitude=dropoff_lat,
  passenger_count=int(passenger_count)
)

response = requests.get(
    url,
    params=params
)

prediction = response.json()

f'This journey will cost approximately ${round(prediction["fare"], 2)}'

dflon = [pickup_lon,dropoff_lon]
dflat = [pickup_lat,dropoff_lat]
df = pd.DataFrame(
    {'longitude':dflon,
     'latitude':dflat})
st.map(df)



# st.markdown('''
# Remember that there are several ways to output content into your web page...

# Either as with the title by just creating a string (or an f-string). Or as with this paragraph using the `st.` functions
# ''')

# '''
# ## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# 1. Let's ask for:
# - date and time
# - pickup longitude
# - pickup latitude
# - dropoff longitude
# - dropoff latitude
# - passenger count
# '''

# '''
# ## Once we have these, let's call our API in order to retrieve a prediction

# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...

# 🤔 How could we call our API ? Off course... The `requests` package 💡
# '''

# url = 'https://taxifare.lewagon.ai/predict'

# if url == 'https://taxifare.lewagon.ai/predict':

#     st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')

# '''

# 2. Let's build a dictionary containing the parameters for our API...

# 3. Let's call our API using the `requests` package...

# 4. Let's retrieve the prediction from the **JSON** returned by the API...

# ## Finally, we can display the prediction to the user
# '''
