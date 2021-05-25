"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

def get_user():
    return auth.current_user.get('id') if auth.current_user else None


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later

db.define_table(
    'users',
    Field('email', default=get_user_email),
    Field('name'),
    Field('social_elo', 'integer', default=0),
    Field('region'),
    Field('microphone', 'boolean', default=False),
    Field('dob'),
)

db.commit()
