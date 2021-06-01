"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
import json
import pgeocode

import crud
import model

from jinja2 import StrictUndefined

from pyzipcode import ZipCodeDatabase

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")

# make a function that finds relevant farms, take in zip code, radius, state as parameters
def find_farms(zip_code, miles, state=None, months=None):
    zcdb = ZipCodeDatabase()

    if zip_code:
        
        nearby_zip_codes = [z.zip for z in zcdb.get_zipcodes_around_radius(str(zip_code), int(miles))]
        farms = []
        for z in nearby_zip_codes:
            farms_per_zip_code = crud.get_farms_by_zip_code(z)
            if farms_per_zip_code:
                for farm in farms_per_zip_code:
                    # print(farm.farm_id)
                   
                    availablities = crud.get_availability_by_farm(farm.farm_id)
                    # print(availablities.first())
                    # print(availablities[0].available_month)
                    available_months = []
                    
                    for availablity in availablities:
                        available_months.append(availablity.available_month)
                        # months here is empty because I am not getting the args....
                print(months)
                print(available_months)
                print(set(months).intersection(available_months))
                if set(months).intersection(available_months):
                    farms.append(farm)
                    # farms.append(farms_per_zip_code)
        print(farms)
        # farms = [farm for sub_list in farms for farm in sub_list]
        # farm_links = [farm.link for farm in farms]

    if state:
        farms = crud.get_farms_by_state(state)
        # farm_links = [farm.link for farm in farms]
    
    farm_list = []
    for farm in farms:
        farm_dict = {}
        farm_dict['name'] = 'tbu'
        farm_dict['lon'] = farm.lon
        farm_dict['lat'] = farm.lat
        farm_dict['link'] = farm.link
        farm_list.append(farm_dict)
    
    return farm_list

def find_coords(zip_code):
    location = pgeocode.Nominatim('us')
    lon = location.query_postal_code (zip_code).longitude
    lat = location.query_postal_code (zip_code).latitude
    return lon, lat

@app.route('/api/farms', methods=["GET", "POST"])
# view function is farms
def farms():
    """return list of relevant farms"""
    # this is empty right now, so I will need to find a way to get zip_code, state, and miles
    # I know I can get all the html using this GET /current_location?zip_code=59821&miles=3&state=
    # but it's probably not what I want to do.
    zip_code = request.form.get('zip_code', None)
    state = request.form.get('state', None)

    # if user doesn't have miles, put in default
    miles = request.form.get('miles', None)

    # print(json.loads(request.form.get('months[]')))
    months = [int(num) for num in request.form.getlist('months[]')]

    farm_lists = find_farms(zip_code=zip_code, miles=miles, state=state, months=months)

    lon, lat = find_coords(zip_code)
    
    return jsonify(lon, lat, farm_lists, miles)

@app.route("/current_location", methods=["GET"])
def current_location():
    """View current location."""
    
    # zip_code = request.args.get('zip_code')
    # state = request.args.get('state')

    # if user doesn't have miles, put in default
    # miles = request.args.get('miles')

    # zcdb = ZipCodeDatabase()

    # if zip_code:
        
    #     nearby_zip_codes = [z.zip for z in zcdb.get_zipcodes_around_radius(str(zip_code), int(miles))]
    #     farms = []
    #     for z in nearby_zip_codes:
    #         farms_per_zip_code = crud.get_farms_by_zip_code(z)
    #         if farms_per_zip_code:
    #             farms.append(farms_per_zip_code)
    #     farms = [farm for sub_list in farms for farm in sub_list]
    #     farm_links = [farm.link for farm in farms]

    # if state:
    #     farms = crud.get_farms_by_state(state)
    #     farm_links = [farm.link for farm in farms]
    
    # this is where I get all the revelant farms
    # return render_template("current-location.html", state=state, zip_code=zip_code, farms=farm_links)
    return render_template("current-location.html")

# @app.route("/map/basic")
# def view_basic_map():
#     """Demo of basic map-related code.

#     - Programmatically adding markers, info windows, and event handlers to a
#       Google Map
#     - Showing polylines, directions, etc.
#     - Geolocation with HTML5 navigator.geolocate API
#     """

#     return render_template("map-basic.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    """create user account."""

    return render_template("create_account.html")

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
    # get user-provided name and password from request.form
    # need to check that user_name doesn't already exist in the database
    user_name = request.form['user_name']
    password = request.form['password']

    user = crud.get_user(user_name=user_name)

    # - if a Customer with that email was found, check the provided password
    #   against the stored one
    if user.user_name != None:
        # - if they match, store the user's email in the session, flash a success
         #   message and redirect the user to the "/" route
        if user.password == password:
            session['customer'] = user_name
            flash("Login successful!")
            return redirect("/")
        # - if they don't, flash a failure message and redirect back to "/login"
        else:
            flash("Incorrect password")
            return redirect("/login")
    # - do the same if a Customer with that email doesn't exist
    else:
        flash("No customer with that email found.")
        return redirect("/login")

@app.route("/logout", methods=["GET", "POST"])
def process_logout():
    session.pop("customer", None)
    print(session.items())
    flash("logged out")
    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
