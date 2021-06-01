from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f'<User id={self.id} user_name={self.user_name}>'

class Image(db.Model):
    """An Image"""

    __tablename__ = 'images'

    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    image = db.Column(db.String) # this will store file paths

    def __repr__(self):
        return f'<Image image_id={self.image_id} user_id={self.user_id}>'



class Entry(db.Model):
    """a user entry"""

    __tablename__ = 'entries'

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    entry = db.Column(db.Text)

    def __repr__(self):
        return f'<Entry entry_id={self.entry_id} user_id={self.user_id}>'

class Location(db.Model):
    """a location"""

    __tablename__ = 'locations'

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    zip_code = db.Column(db.Integer)

    def __repr__(self):
        return f'<Location location_id={self.location_id} zip_code={self.zip_code}>'

class CurrentLocation(db.Model):
    """current location of a user"""

    __tablename__ = 'current_locations'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))

class Farm(db.Model):
    """a farm entry"""

    __tablename__ = 'farms'

    farm_id = db.Column(db.Integer, primary_key=True)
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)
    state = db.Column(db.String)
    zip_code = db.Column(db.Integer)
    link = db.Column(db.String)

    def __repr__(self):
        return f'<Farm farm_id={self.farm_id} state={self.state} zip_code={self.zip_code}>'

class FarmAvailability(db.Model):
    """shows farm availability"""

    __tablename__ = 'farm_availabilities'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.farm_id'))
    available_month = db.Column(db.Integer)


def connect_to_db(flask_app, db_uri='postgresql:///farms', echo=True):
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = flask_app
    db.init_app(flask_app)

    print('Connected to the db!')


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
