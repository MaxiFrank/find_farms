"""CRUD operations."""

from model import db, User, Image, Entry, Location, CurrentLocation, Farm, FarmAvailability, connect_to_db

def create_user(user_name, password):
    """Create and return a new user"""

    user = User(user_name=user_name, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def create_image(user_id, image):
    """Create and return a new image"""

    image = Image(user_id=user_id, image=image)

    db.session.add(image)
    db.session.commit()

    return image

def create_entry(user_id, entry):
    """create a user entry and return the entry"""

    entry = Entry(user_id=user_id, entry=entry)

    db.session.add(entry)
    db.session.commit()

    return entry

def create_location(user_id, lon, lat, state):
    """create location"""

    location = Location(user_id=user_id, lon=lon, lat=lat, state=state)

    db.session.add(location_id)
    db.session.commit()

    return location

def create_current_location(user_id, location_id):
    """create current location for user"""

    current_location = CurrentLocation(user_id=user_id, location_id=location_id)

    db.session.add(current_location)
    db.session.commit()

    return current_location

def create_farm(lon, lat, state, zip_code, link):
    """create farm with a link to images in the static folder"""

    farm = Farm(lon=lon, lat=lat, state=state, zip_code=zip_code, link=link)

    db.session.add(farm)
    db.session.commit()

    return farm

def create_farm_availablity(farm_id, available_month):
    """create farm availabilty for each farm, at most 12 entries per farm"""

    farm_availability = FarmAvailability(farm_id=farm_id, available_month=available_month)

    db.session.add(farm_availability)

    db.session.add(farm_availability)
    db.session.commit()

    return farm_availability

def get_farms_by_state(state):
    """Return farms by state."""
    return Farm.query.filter(Farm.state == state).all()

def get_farms_by_zip_code(zip_code):
    """Return farms by zip code."""

    return Farm.query.filter(Farm.zip_code == zip_code).all()

def get_availability_by_farm(farm_id):
    return FarmAvailability.query.filter(FarmAvailability.farm_id == farm_id).all()

def get_user(user_name):
    """Return farms by zip code."""

    return User.query.filter(User.user_name == user_name).first()

def get_farms_by_user_id(user_id):
    """Return farms by zip code."""

    return Entry.query.filter(Entry.user_id == user_id).all()

def get_farm_by_url(link):
    """Return farms by zip code."""

    return Farm.query.filter(Farm.link == link).first()