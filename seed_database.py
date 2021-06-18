"""Script to seed database"""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

import geopy

os.system('dropdb farms')
os.system('createdb farms')

model.connect_to_db(server.app)
model.db.create_all()


with open('data/farms_scrape.json') as f:
    farm_data = json.loads(f.read())

farms_in_db = []
farms_available_months_in_db = []

geolocator = geopy.Nominatim(user_agent='__main__')

for farm in farm_data:

    lat = farm['lat']
    lon = farm['lon']
    link = farm['link']
    title = farm['title']
    # determine if I want to use the unique identifier from workaway later
    # farm_id = int(link.split('/')[-1])
    available_months = farm['available_months']

    try:
        location = geolocator.reverse((float(lat), float(lon)))

    except:
        continue

    else:
        if location:

            state = location.raw['address']['state']
            
            if 'postcode' in location.raw['address'].keys():
                zip_code = str(location.raw['address']['postcode'][0:5])
            else:
                zip_code = None


        db_farm = crud.create_farm(lon=lon, lat=lat, state=state, zip_code=zip_code, link=link, title=title)
        # only need append if I need to create more fake data
        # farms_in_db.append(db_farm)

        for available_month in available_months:
            farm_id = int(db_farm.farm_id)
            db_farm_available_month = crud.create_farm_availablity(farm_id, available_month)
            # only need append if I need to create more fake data
            # farms_available_months_in_db.append(db_farm_available_month)

