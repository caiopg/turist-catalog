import random
import string

import httplib2
import requests
from flask import Flask, render_template, request, url_for, jsonify, \
    session as login_session, json, make_response
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect

from db_setup import Base, DB_PATH, Country, Attraction

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'][
    'client_id']

engine = create_engine(DB_PATH)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/countries/')
def home():
    countries = session.query(Country)

    state = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for x in
        range(32))

    login_session['state'] = state

    return render_template('home.html', countries=countries,
                           state=login_session['state'])


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        print("Error in access token info")
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'),
            200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    return ''


@app.route('/countries/<int:country_id>/')
def show_country(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    attractions = session.query(Attraction).filter_by(
        country_id=country_id).all()

    return render_template('country.html', country=country,
                           attractions=attractions)


@app.route('/countries/<int:country_id>/json/')
def country_json(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    attractions = session.query(Attraction).filter_by(
        country_id=country_id).all()

    return jsonify(Country=country.serialize,
                   Attractions=[a.serialize for a in attractions])


@app.route('/countries/<int:country_id>/edit/',
           methods=['GET', 'POST'])
def edit_country(country_id):
    country = session.query(Country).filter_by(id=country_id).one()

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        session.add(country)
        session.commit()

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('editcountry.html', country=country)


@app.route('/countries/<int:country_id>/delete/', methods=['GET', 'POST'])
def delete_country(country_id):
    country = session.query(Country).filter_by(id=country_id).one()

    if request.method == 'POST':
        session.query(Attraction).filter_by(
            country_id=country_id).delete()

        session.delete(country)
        session.commit()

        return redirect(url_for('home'))

    return render_template('deletecountry.html', country=country)


@app.route('/countries/new', methods=['GET', 'POST'])
def new_country():
    if request.method == 'POST':
        inputs = request.form
        country = Country()

        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        session.add(country)
        session.commit()

        return redirect(url_for('home'))

    return render_template('newcountry.html')


@app.route('/countries/<int:country_id>/<int:attraction_id>/')
def show_attraction(country_id, attraction_id):
    country = session.query(Country).filter_by(id=country_id).one()
    attraction = session.query(Attraction).filter_by(id=attraction_id).one()

    return render_template('attraction.html', country=country,
                           attraction=attraction)


@app.route('/countries/<int:country_id>/<int:attraction_id>/edit/',
           methods=['GET', 'POST'])
def edit_attraction(country_id, attraction_id):
    attraction = session.query(Attraction).filter_by(id=attraction_id).one()
    country = session.query(Country).filter_by(id=country_id).one()
    countries = session.query(Country)

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            attraction.name = inputs['name']
        if inputs['city']:
            attraction.city = inputs['city']
        if inputs['description']:
            attraction.description = inputs['description']

        session.add(attraction)
        session.commit()

        return redirect(url_for('show_attraction', country_id=country_id,
                                attraction_id=attraction_id))

    return render_template('editattraction.html', attraction=attraction,
                           country=country, countries=countries)


@app.route('/countries/<int:country_id>/<int:attraction_id>/delete/',
           methods=['GET', 'POST'])
def delete_attraction(country_id, attraction_id):
    attraction = session.query(Attraction).filter_by(id=attraction_id).one()
    country = session.query(Country).filter_by(id=country_id).one()

    if request.method == 'POST':
        attraction = session.query(Attraction).filter_by(
            id=attraction_id).one()
        session.delete(attraction)

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('deleteattraction.html', attraction=attraction,
                           country=country)


@app.route('/countries/<int:country_id>/new/', methods=['GET', 'POST'])
def new_attraction(country_id):
    country = session.query(Country).filter_by(id=country_id).one()

    if request.method == 'POST':
        inputs = request.form
        attraction = Attraction()

        if inputs['name']:
            attraction.name = inputs['name']
        if inputs['city']:
            attraction.city = inputs['city']
        if inputs['description']:
            attraction.description = inputs['description']

        attraction.country = country

        session.add(attraction)
        session.commit()

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('newattraction.html', country=country)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "my_name_is_goku"
    app.run(host='0.0.0.0', port=8000)
