#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
import sys
import pprint
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.PickleType, nullable=True)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    image_link = db.Column(db.String(500), nullable=False)
    website = db.Column(db.String(120), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='venue', lazy='dynamic')

  #added seeking_talent , seeking_description and Webiste Columns
  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120) ,nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(db.PickleType, nullable=True)
    image_link = db.Column(db.String(500) ,nullable=True)
    facebook_link = db.Column(db.String(120) ,nullable=True)
    website = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(500), nullable=True)
    shows = db.relationship('Show', backref='artist', lazy='dynamic')
    
  #added seeking_talent , seeking_description and Webiste Columns

# TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

# Created the Show Model
class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'),nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'),nullable=False)
    date = db.Column(db.DateTime(), nullable=False )
  #added name and date(start_time) columns to the show tabel
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_shows should be aggregated based on number of upcoming shows per venue.

  data=[{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  #fetched Venues and group by id, state and city so that similar cities and states can follow each other
  all_venues = Venue.query.group_by(Venue.id, Venue.state, Venue.city).all()
  city = ''
  state = ''
  # Get the Time Now
  time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  data=[]  
  # Implemented for loop to loop through the venue and group the venues based on city and state
  for index, venue in enumerate(all_venues):
    upcoming_show_query = venue.shows.filter(Show.date > time_now)
    upcoming_shows =upcoming_show_query.all()
    num_upcoming_shows =upcoming_show_query.count()
    # Check if the city ad state are equal to the stored city and state 
    if venue.state == state and venue.city == city:
      data_length = len(data)

      # Appending to data.venue where both city and state are equal or similar
      data[data_length - 1]['venues'].append({
        'id': venue.id,
        'name': venue.name,
        'num_upcoming_shows' :num_upcoming_shows
      })      
      # There's no need to set the city and state as they are already the same as what is current stored
    else:
      # since state and city are not similar this but be a state anad city with no similar values
      data.append({
        'state': venue.state,
        'city': venue.city,
        'venues': [{
          'id':venue.id,
          'name':venue.name,
          'num_upcoming_shows': num_upcoming_shows
        }]
      })
      # storing new state and city for comparison in next iteration
      city = venue.city
      state = venue.state

   
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  # Get the search term using request.form.get
  search_term = request.form.get('search_term', '')
  # Using ilike for insensitive name search
  search = Venue.query.filter(Venue.format().name.ilike('%{}%'.format(search_term)))
  data = search.all()
  # Calculating count for search items
  count = search.count()
  # Arranging the data in the appropiate manner
  response={
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term= search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  # getting the current Date and Time
  time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  # getting the venue with this particular venue id
  data = Venue.query.get(venue_id)
  # Get upcoming shows for this venue
  upcoming_show_query = data.shows.filter(Show.date > time_now)
  upcoming_shows = upcoming_show_query.all()
  data.upcoming_shows_count = upcoming_show_query.count()
  # iterating over upcoming shows to properly construct upcoming show object for use by frontend
  for show in upcoming_shows:
    show.artist_name = show.artist.name
    show.artist_image_link = show.artist.image_link
    show.start_time = show.date.strftime("%d %b, %Y")
  data.upcoming_shows = upcoming_shows 

  # get past shows for this venue
  past_show_query = data.shows.filter(Show.date < time_now)
  past_shows = past_show_query.all()
  data.past_shows_count = past_show_query.count()
  # get artist details by using show artist relationship
  # iterating over past shows to properly coonstruct object for frontend
  for show in past_shows:
    show.artist_name = show.artist.name
    show.artist_image_link = show.artist.image_link
    show.start_time = show.date.strftime("%d %b, %Y")
  data.past_shows = past_shows
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  try:
    # get the venue form details
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    address = request.form['address']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']
    website = request.form['website']
    # check to see if user check the seeking talent checkbox and setting value to True/False
    if 'seeking_talent' in request.form:
      seeking_talent = (request.form['seeking_talent']=='y')
    else:
      seeking_talent = False    
    seeking_description = request.form['seeking_description']

    # Inserting new venue into the database
    venue = Venue(name=name, city=city, state=state, phone=phone, genres=genres,address=address,
    image_link=image_link, facebook_link=facebook_link, website=website, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()
    # Flash successful insertion
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    db.session.rollback()
    print(sys.exc_info())    
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    # on successful db insert, flash success
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  status = True
  try:
    # Getting venue by venue_id
    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    # deleting venue
    db.session.delete(venue)
    db.session.commit()
  except:
    status = False
    flash('Venue was not successfully deleted!')
    db.rollback()  
  finally:
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    flash(venue_name + ' venue was successfully deleted!')
    return jsonify({
      'status': status
    })   


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  # Get all artists in the Database
  artist = Artist.query.all()
  return render_template('pages/artists.html', artists=artist)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  # get search term
  search_term = request.form.get('search_term', '')
  # search for artist using ilike for case insensitive search
  search = Artist.query.filter(Venue.name.ilike('%{}%'.format(search_term)))
  # Return artists and artist count
  data = search.all()
  count = search.count()
  response={
    "count": count,
    "data": data
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  # get the current date and time and convert to appropiate format
  time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  # get artist by artist id
  data = Artist.query.get(artist_id)
  # get artist upcoming show using relationship
  upcoming_show_query = data.shows.filter(Show.date > time_now)
  upcoming_shows = upcoming_show_query.all()
  data.upcoming_shows_count = upcoming_show_query.count()
  # loop through show to properly construct object
  for show in upcoming_shows:
    show.venue_name = show.venue.name
    show.venue_image_link = show.venue.image_link
    show.start_time = show.date.strftime("%d %b, %Y")
  data.upcoming_shows = upcoming_shows
  # get past shows using show time to filter
  past_show_query = data.shows.filter(Show.date < time_now)
  past_shows = past_show_query.all()
  data.past_shows_count = past_show_query.count()
  # get venue details by using relationship
  # loop through show to properly construct object
  for show in past_shows:
    show.venue_name = show.venue.name
    show.venue_image_link = show.venue.image_link
    show.start_time = show.date.strftime("%d %b, %Y")
  data.past_shows = past_shows
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  # populating artist form with prexisting data from the database for use on edit page
  artist = Artist.query.get(artist_id)
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  form.genres.data = artist.genres
  form.facebook_link.data = artist.facebook_link 
  form.website.data = artist.website
  form.seeking_venue.data = artist.seeking_venue
  form.seeking_description.data = artist.seeking_description
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    # get submitted data
    artist = Artist.query.get(artist_id)
    artist.name = request.form['name']
    artist.city = request.form['city']
    artist.state = request.form['state']
    artist.phone = request.form['phone']
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form['facebook_link']
    # check if user checked the seeking talet checkbox
    if 'seeking_venue' in request.form:
      artist.seeking_venue = (request.form['seeking_venue']=='y')
    else:
      artist.seeking_venue = False    
    artist.seeking_description = request.form['seeking_description']
    artist.website = request.form['website']
    db.session.commit()
    flash('Artist ' + artist.name + ' was updated successfully.')
  except:
    # flash error if unsuccessful commit
    flash('An error occurred. Artist ' + artist.name + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  # populating the edit venue form with prexisting data fro the database
  venue = Venue.query.get(venue_id)
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  form.website.data = venue.website
  form.seeking_talent.data = venue.seeking_talent
  form.seeking_description.data = venue.seeking_description
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    # get venue values submitted
    venue = Venue.query.get(venue_id)
    venue.name = request.form['name']
    venue.city = request.form['city']
    venue.state = request.form['state']
    venue.address = request.form['address']
    venue.phone = request.form['phone']
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form['facebook_link']
    # check if user checked the seeking_talent checkbox
    if 'seeking_talent' in request.form:
      venue.seeking_talent = (request.form['seeking_talent']=='y')
    else:
      venue.seeking_talent = False    
    venue.seeking_description = request.form['seeking_description']
    venue.website = request.form['website']
    db.session.commit()
    # flash success if commit passes
    flash('Venue ' + venue.name + ' was updated successfully.')
  except:
    # flash error if commit fails
    flash('An error occurred. Artist ' + venue.name + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form  
  # TODO: insert form data as a new Venue record in the db, instead
  try:
    # get submitted data from the create artit form
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    phone = request.form['phone']
    genres = request.form.getlist('genres')
    image_link = request.form['image_link']
    facebook_link = request.form['facebook_link']  
    website = request.form['website']
    # check if user check the seeking venue check box
    if 'seeking_talent' in request.form:
      seeking_venue = (request.form['seeking_venue']=='y')
    else:
      seeking_venue = False    
    seeking_description = request.form['seeking_description']
    artist = Artist(name=name, city=city, state=state, phone=phone, genres=genres, image_link=image_link, 
    facebook_link=facebook_link,website=website, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except:
    db.session.rollback()
    print(sys.exc_info())
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')   
    # TODO: modify data to be the data object returned from db insertion
  finally:
    # on successful db insert, flash success
    # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')

@app.route('/artist/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a artist_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  status = True
  try:
    # get the artist by id
    artist = Artist.query.get(artist_id)
    artist_name = artist.name
    # delete queried artist
    db.session.delete(artist)
    db.session.commit()
  except:
    status = False
    # flash error and rollback if commit failed
    flash('artist was not successfully deleted!')
    db.rollback()
    print(sys.exc_info())

  finally:
    # BONUS CHALLENGE: Implement a button to delete a artist on a artist Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    flash(artist_name + ' was successfully deleted!')
    return jsonify({
      'status': status
    })   



#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  # get all shows in the db
  shows = Show.query.all()
  # construct show object to match dummy data
  for show in shows:
    show.artist_name = show.artist.name
    show.venue_name = show.venue.name
    show.artist_image_link = show.artist.image_link
    show.start_time = show.date.strftime("%d %b, %Y")
  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  try:
    # get artist and venues using submitted ids
    artist_count = Artist.query.filter_by(id =request.form['artist_id']).count()
    venue_count = Venue.query.filter_by(id =request.form['venue_id']).count()
    print(artist_count, venue_count)
    # check if artist and venue exist in the db and flash errors if any of the ids are invalid
    if artist_count == 0:
      flash('Error Occured. Artist ID is Invalid, Please check for appropiate Artist IDs')
    if venue_count == 0:
      flash('Error Occured. Venue ID is Invalid, Please check for appropiate Venue IDs')
    else:
      # create show using valid artist and venue id
      artist_id = request.form['artist_id']
      venue_id = request.form['venue_id']
      name = request.form['name']
      date = request.form['start_time']    
      show = Show(name=name,artist_id=artist_id, venue_id=venue_id, date=date)
      db.session.add(show)
      db.session.commit()
      flash(name + ' show was successfully listed!')    
  except:
    db.rollback()
    print(sys.exc_info())     
    flash('Error Occured. Show could not listed!')
  finally:
    # on successful db insert, flash success
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    # return render_template('pages/home.html')
    return render_template('pages/home.html')

@app.route('/shows/search', methods=['POST'])
def search_shows():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  # get the search term which is the name of the show
  search_term = request.form.get('search_term', '')
  # filter using ilike for case insensitive search
  search = Show.query.filter(Show.name.ilike('%{}%'.format(search_term)))
  # return shows and show count
  data = search.all()
  count = search.count()
  # get artist and venue data using relationship
  # construct show object to match front end
  for show in data:
    show.artist_name = show.artist.name
    show.venue_name = show.venue.name
    show.artist_image_link = show.artist.image_link
    show.start_time = show.date.strftime("%d %b, %Y")

  # return render_template('pages/show.html', results=response, search_term= search_term)
  return render_template('pages/show.html', shows=data, count=count, search_term=request.form.get('search_term', ''))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
