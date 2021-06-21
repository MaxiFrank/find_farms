"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from jinja2.runtime import LoopContext
from model import connect_to_db
import json
import pgeocode

import crud
import model
import os

from jinja2 import StrictUndefined

from pyzipcode import ZipCodeDatabase

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined
# SESSION_COOKIE_HTTPONLY = False

# session.cookie_httponly=on

@app.route("/")
def homepage():
    """View homepage."""
    return render_template("homepage.html")

def find_farms(zip_code=None, miles=None, state=None, months=None):
    """finds relevant farms, take in zip code, radius, state as parameters"""

    zcdb = ZipCodeDatabase()

    # not sure if this solves the problem
    if not miles:
        miles = 10
    if not months:
        months = [1,2,3,4,5,6,7,8,9,10,11,12]

    username = session['customer']
    farm_ids = [None]
    if username:
    # get a list of farm ids
        # get username from user_id
        user_id = crud.get_user(username).id
        # get farms from entry table
        farms_raw = crud.get_farms_by_user_id(user_id)
        # get farm links
        farm_links = [farm.entry for farm in farms_raw]
        # get farms from farm links
        farms_entry = [crud.get_farm_by_url(farm_link) for farm_link in farm_links]
        # get farm ids
        farm_ids = [farm.farm_id for farm in farms_entry]

    
    if zip_code:
        
        nearby_zip_codes = [z.zip for z in zcdb.get_zipcodes_around_radius(str(zip_code), int(miles))]
        farms = []
        for z in nearby_zip_codes:
            farms_per_zip_code = crud.get_farms_by_zip_code(z)
            if farms_per_zip_code:
                for farm in farms_per_zip_code:
                    if farm.farm_id not in farm_ids:
                        availablities = crud.get_availability_by_farm(farm.farm_id)
                        available_months = []
                        
                        for availablity in availablities:
                            available_months.append(availablity.available_month)

                        if set(months).intersection(available_months):
                            farms.append(farm)

    if state:
        farms = []
        state_farms = crud.get_farms_by_state(state)
        for farm in state_farms:
            if farm.farm_id not in farm_ids:
    
                availablities = crud.get_availability_by_farm(farm.farm_id)
                
                available_months = []
                for availablity in availablities:
                    available_months.append(availablity.available_month)


                if set(months).intersection(available_months):
                    farms.append(farm)


    farm_list = []
    for farm in farms:

        farm_dict = {}
        farm_dict['name'] = 'tbu'
        farm_dict['lon'] = farm.lon
        farm_dict['lat'] = farm.lat
        farm_dict['link'] = farm.link
        farm_dict['title'] = farm.title
        farm_list.append(farm_dict)

    return farm_list

def find_coords(zip_code=None, state=None):
    location = pgeocode.Nominatim('us')
    if zip_code:
        lon = location.query_postal_code(zip_code).longitude
        lat = location.query_postal_code(zip_code).latitude
    if state:
        farm = crud.get_farm_by_state(state)[0]
        lon = farm.lon
        lat = farm.lat
    return lon, lat

@app.route('/api/farms', methods=["GET", "POST"])
def farms():
    """return list of relevant farms"""
    zip_code = request.form.get('zip_code', None)
    state = request.form.get('state', None)
    miles = request.form.get('miles', None)
    months = [int(num) for num in request.form.getlist('months[]')]

    farm_lists = find_farms(zip_code=zip_code, miles=miles, state=state, months=months)

    lon, lat = find_coords(zip_code,state)
    
    return jsonify(lon, lat, farm_lists, miles)

@app.route('/api/bookmark', methods=["GET", "POST"])
def bookmark():
    """return list of relevant farms"""
    print(session)
    user_name = session['customer']

    if user_name:
        current_link = request.form.get('current-link', None)
        current_title = request.form.get('current-title', None)
        user_id = crud.get_user(user_name).id
        crud.create_entry(user_id=user_id, entry=current_link, title=current_title)
        return jsonify(current_link)
    else:
        return ''

@app.route("/current_location", methods=["GET"])
def current_location():
    """View current location."""

    GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
    # print('printing session info')
    # print(session.items())
    # states = crud.get_states()
    # print(states)
    return render_template("current-location.html", GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)

@app.route("/current_location_state", methods=["GET"])
def current_location_by_state():
    """View current location."""

    GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
    print('printing session info')
    print(session.items())
    states = crud.get_states()
    print(states)
    states = [state for state in states if state!= "Дорноговь"]
    return render_template("current-location-state.html", GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY, states=states)

@app.route("/create_account", methods=["GET"])
def create_account_get():
    """create user account."""

    return render_template("create_account.html")

@app.route("/create_account", methods=["POST"])
def create_account_post():
    """create user account."""
    user_name = request.form.get('user_name')
    password = request.form.get('password')

    crud.create_user(user_name, password)

    return redirect("/")

@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """
    user_name = request.form['user_name']
    password = request.form['password']

    user = crud.get_user(user_name=user_name)


    if user.user_name != None:
        if user.password == password:
            session['customer'] = user_name
            flash("Login successful!")
            return redirect("/")

        else:
            flash("Incorrect password")
            return redirect("/login")

    else:
        flash("No customer with that email found.")
        return redirect("/login")

@app.route("/logout", methods=["GET", "POST"])
def process_logout():
    session['customer'] = None
    flash("logged out")
    return redirect("/")

@app.route("/favorite")
def list_farms():
    """create user account."""
    username = session['customer']
    farms = []
    user_id = crud.get_user(username).id
    entry_farms = crud.get_farms_by_user_id(user_id)
    for entry_farm in entry_farms:
        link = entry_farm.entry
        farm = crud.get_complete_farm_from_entry(link)
        farms.append(farm)
    return render_template("bookmarked.html", farms=farms)

@app.route("/about")
def story():
    """create user account."""

    return render_template("about.html")

@app.route("/api/bookmarked", methods=["GET"])
def show_existing_favorites():
    """create user account."""
    username = session['customer']
    # get username from user_id
    user_id = crud.get_user(username).id
    # get farms from entry table
    farms_raw = crud.get_farms_by_user_id(user_id)
    # get farm links
    farm_links = [farm.entry for farm in farms_raw]
    # get farms from farm links
    farms = [crud.get_farm_by_url(farm_link) for farm_link in farm_links]
    # print(farms)
    farm_list = []

    for farm in farms:
        farm_dict = {}
        farm_dict['center_lon'] = -98.5795
        farm_dict['center_lat'] = 39.8283
        farm_dict['lon'] = farm.lon
        farm_dict['lat'] = farm.lat
        farm_dict['link'] = farm.link
        farm_dict['zoom'] = 4
        farm_list.append(farm_dict)

    return jsonify(farm_list)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)