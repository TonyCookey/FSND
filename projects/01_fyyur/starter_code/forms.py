from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, ValidationError, TextAreaField, BooleanField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, AnyOf, URL, Regexp, Length
from enum import Enum

class Genre(Enum):
    Alternative = 'Alternative'
    Blues = 'Blues'
    Classical = 'Classical'
    Country = 'Country'
    Electronic =' Electronic'
    Folk = 'Folk'
    Funk = 'Funk'
    HipHop = 'Hip-Hop'
    HeavyMetal = 'Heavy Metal'
    Instrumental = 'Instrumental'
    Jazz = 'Jazz'
    MusicalTheatre = 'Musical Theatre'
    Pop = 'Pop'
    Punk = 'Punk'
    RnB = 'R&B'
    Reggae = 'Reggae'
    RocknRoll = 'Rock n Roll'
    Soul = 'Soul'
    Other = 'Other'

    @classmethod
    def genres(cls):
        return [(choice.name, choice.value) for choice in cls]

class ShowForm(Form):
    artist_id = StringField(
        'artist_id', validators=[DataRequired()]
    )
    venue_id = StringField(
        'venue_id', validators=[DataRequired()]
    )
    # Adding Name of Show 
    name = StringField(
        'name', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone' , validators=[DataRequired()] 
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices = Genre.genres()
        # choices=[
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    website = StringField(
        'website', validators=[URL()]
    )  
    # Using Boolen Fields for the seeking talent
    seeking_talent =BooleanField(
        'seeking_talent', default="checked"
    )
    seeking_description = TextAreaField(
        'seeking_description'
    )

class ArtistForm(Form):
    
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[DataRequired()]               
    )
    
    image_link = StringField(
        'image_link', validators=[URL(),DataRequired()]
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices = Genre.genres()

        # choices=[
        #     ('Alternative', 'Alternative'),
        #     ('Blues', 'Blues'),
        #     ('Classical', 'Classical'),
        #     ('Country', 'Country'),
        #     ('Electronic', 'Electronic'),
        #     ('Folk', 'Folk'),
        #     ('Funk', 'Funk'),
        #     ('Hip-Hop', 'Hip-Hop'),
        #     ('Heavy Metal', 'Heavy Metal'),
        #     ('Instrumental', 'Instrumental'),
        #     ('Jazz', 'Jazz'),
        #     ('Musical Theatre', 'Musical Theatre'),
        #     ('Pop', 'Pop'),
        #     ('Punk', 'Punk'),
        #     ('R&B', 'R&B'),
        #     ('Reggae', 'Reggae'),
        #     ('Rock n Roll', 'Rock n Roll'),
        #     ('Soul', 'Soul'),
        #     ('Other', 'Other'),
        # ]
    )
    # using URL validators for the facebook field
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )
    # using URL validators for the webiste field

    website = StringField(
        'website', validators=[URL()]
    )   
    # using boolean field for the seeking venue field
    seeking_venue =BooleanField(
        'seeking_venue', default="checked"
    )
    seeking_description = TextAreaField(
        'seeking_description'
    )

# TODO IMPLEMENT NEW ARTIST FORM AND NEW SHOW FORM
