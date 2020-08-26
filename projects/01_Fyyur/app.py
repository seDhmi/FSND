#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (
  Flask,
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for, 
  abort,
  jsonify
  )
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy import func
from flask_migrate import Migrate
import sys

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
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    image_link = db.Column(db.String(500), nullable=False)
    facebook_link = db.Column(db.String(120), unique=True)
    shows = db.relationship('Show', backref='venue',lazy=True)
    genres = db.Column(db.ARRAY(db.String()))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    @property
    def past_shows(self):
      now = datetime.now()
      pastShows = [i for i in self.shows if datetime.strptime(
        i.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return pastShows

    @property
    def upComing_shows(self):
      now = datetime.now()
      upComingShows = [i for i in self.shows if datetime.strptime(
        i.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return upComingShows

    @property
    def past_shows_count(self):
      return len(self.past_shows)

    @property
    def upComing_shows_count(self):
      return len(self.upComing_shows)


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), unique=True)
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120), unique=True, nullable = True)
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    @property
    def past_shows(self):
      now = datetime.now()
      pastShows = [i for i in self.shows if datetime.strptime(
        i.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return pastShows


    @property
    def upComing_shows(self):
      now = datetime.now()
      upComingShows = [i for i in self.shows if datetime.strptime(
        i.start_time, '%Y-%m-%d %H:%M:%S') < now]
      return upComingShows


    @property
    def past_shows_count(self):
      return len(self.past_shows)


    @property
    def upComing_shows_count(self):
      return len(self.upComing_shows)

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.String(), nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

  @property
  def artist_name(self):
    artist = Artist.query.get(self.artist_id)
    return artist.name


  @property
  def venue_name(self):
    venue = Venue.query.get(self.venue_id)
    return venue.name


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
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  uniqueCS = Venue.query.with_entities(Venue.city, Venue.state).distinct().all()

  data=[]

  for CS in uniqueCS:
    venues = Venue.query.filter_by(city=CS[0], state=CS[1]).all()
    data.append({'city': CS[0], 'state': CS[1], 'venues': venues})

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  venues = Venue.query.filter_by(func.lower(Venue.name).contains(
    request.form.get('search_term').lower())).all()

  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)

  past_shows = list(filter(lambda x: x.start_time < datetime.today(), venue.shows))
  upcoming_shows = list(filter(lambda x: x.start_time >= datetime.today(), venue.shows))

  past_shows = list(map(lambda x: x.show_artist(), past_shows))
  upcoming_shows = list(map(lambda x: x.show_artist(), upcoming_shows))

  data = venue.venue_to_dictionary()

  data['past_shows'] = past_shows
  data['past_shows_count'] = len(past_shows)

  data['upcoming_shows'] = upcoming_shows
  data['upcoming_shows_count'] = len(upcoming_shows)
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

    error = False
    try:
      if request.form.get('seeking_talent') == 'y':
        seeking_talent = True
      else:
        seeking_talent = False

      venue = Venue(
        name = request.form.get('name'),
        city = request.form.get('city'),
        state = request.form.get('state'),
        address = request.form.get('address'),
        phone = request.form.get('phone', ''),
        genres = request.form.getlist('genres'),
        facebook_link = request.form.get('facebook_link', ''),
        seeking_talent = seeking_talent,
        seeking_description = request.form.get('seeking_description', ''),
        website = request.form.get('website', '')
      )
      db.session.add(venue)
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    except:
      error = True
      db.session.rollback()
      print(sys.exc_info())
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    else:
      return render_template('pages/home.html')

  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artists = Artist.query.filter(func.lower(Artist.name).contains(request.form.get('search_term').lower())).all()

  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data = Artist.query.filter_by(id=artist_id).outerjoin(Show).order_by(Show.start_time).outerjoin(Venue).one()
  upComing_shows = []
  past_shows = []

  for show in data.artist_shows:
    if show.start_time >= datetime.now():
      upComing_shows.append({
        "venue_image_link": show.venue_shows.image_link,
        "venue_id": show.venue_id,
        "venue_name": show.venue_shows.name,
        "start_time": format_datetime(str(show.start_time))
      })
    elif show.start_time < datetime.now():
      past_shows.append({
        "venue_image_link": show.venue_shows.image_link,
        "venue_id": show.venue_id,
        "venue_name": show.venue_shows.name,
        "start_time": format_datetime(str(show.start_time))
      })
    else:
      print('show unprocessed')

  data.upcoming_shows_count = len(upcoming_shows)
  data.upcoming_shows = upcoming_shows
  data.past_shows_count = len(past_shows)
  data.past_shows = past_shows

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist= Artist.query.get(artist_id)
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  error = False
  try:
    if request.form.get('seeking_venue') == 'y':
      seeking_venue = True
    else:
      seeking_venue = False

    artist=Artist.query.get(artist_id)
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone', '')
    artist.genres = request.form.getlist('genres')
    artist.facebook_link = request.form.get('facebook_link', '')
    artist.image_link = request.form.get('image_link', '')
    artist.website = request.form.get('website', '')
    artist.seeking_venue = seeking_venue
    artist.seeking_description = request.form.get('seeking_description', '')
    print(artist.name)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    return flash('An error occurred. Artist ' + request.form.get('name') + ' could not be edited.')
  else:
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    if request.form.get('seeking_talent') == 'y':
      seeking_talent = True
    else:
      seeking_talent = False

    venue=Venue.query.get(venue_id)
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address', '')
    venue.phone = request.form.get('phone', '')
    venue.genres = request.form.getlist('genres')
    venue.facebook_link = request.form.get('facebook_link', '')
    venue.image_link = request.form.get('image_link', '')
    venue.website = request.form.get('website', '')
    venue.seeking_talent = seeking_talent
    venue.seeking_description = request.form.get('seeking_description', '')
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info)
  finally:
    db.session.close()
  if error:
    return flash('An error occurred. Artist ' + request.form.get('name') + ' could not be edited.')
  else:
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
  # TODO: modify data to be the data object returned from db insertion

  error = False

  try:
    if request.form.get('seeking_venue') == 'y':
        seeking_venue = True
    else:
        seeking_venue = False

    artist = Artist(
        name = request.form.get('name'),
        city = request.form.get('city'),
        state = request.form.get('state'),
        phone = request.form.get('phone', ''),
        genres = request.form.getlist('genres'),
        facebook_link = request.form.get('facebook_link', ''),
        image_link = request.form.get('image_link', ''),
        website = request.form.get('website', ''),
        seeking_venue = seeking_venue,
        seeking_description = request.form.get('seeking_description', '')
      )
    print(artist.name)
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    return flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
  else: # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')

@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
      Artist.query.filter_by(id=artist_id).delete()
      db.session.commit()
    except:
      db.session.rollback()
    finally:
      db.session.close()
    return redirect(url_for('index'))

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data= Show.query.order_bt('id').all()
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  error = False

  try:
    newShow = Show(
      artist_id = request.form.get('artist_id'),
      venue_id = request.form.get('venue_id'),
      start_time = request.form.get('start_time')
    )
    db.session.add(newShow)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    return flash('An error occurred. Show could not be listed.')
  # on successful db insert, flash success
  flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')


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
