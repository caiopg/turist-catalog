import random
import string

from flask import Blueprint, render_template
from flask import session as login_session

from db import dbhelper

home_service = Blueprint(name='home', import_name=__name__)

db_helper = dbhelper.DbHelper()


@home_service.route('/')
@home_service.route('/countries/')
def home():
    """
    home() serves the homepage.

    :return: home template
    """

    countries = db_helper.get_countries()

    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None:
        return render_template('loggedhome.html', countries=countries)

    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(32))

    login_session['state'] = state

    return render_template('home.html', countries=countries,
                           state=login_session['state'])
