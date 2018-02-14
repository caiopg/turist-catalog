import random
import string

import httplib2
import requests
from flask import Flask, render_template, request, url_for, jsonify, \
    session as login_session, json, make_response
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets
from werkzeug.utils import redirect

import dbhelper
from dbsetup import Country, Attraction, User

'''webserver is responsible for initiating Flask. It is also responsible
for retreiving the correct html pages, populating them with the correct
elements and serving the browser.'''

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web'][
    'client_id']

db_helper = dbhelper.DbHelper()

'''home() serves the homepage. Template changes if user is logged or not.'''


@app.route('/')
@app.route('/countries/')
def home():
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


'''gdisconnect() disconnects the user from google service.'''


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')

    if access_token is None:
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Call the google url responsible for invalidating the token.
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
          login_session['access_token']
    web = httplib2.Http()
    result = web.request(url, 'GET')[0]

    # Remove all information if url call is successful. Show error if
    # unsuccessful,
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        return redirect(url_for('home'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'))
        response.headers['Content-Type'] = 'application/json'
        return response


'''gconnect() connects the user through the google service.'''


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
    login_session['email'] = data['email']

    user = db_helper.get_user_by_email(data['email'])
    if user is None:
        user_id = create_user(name=data['name'], email=data['email'])
    else:
        user_id = user.id

    login_session['user_id'] = user_id

    return ''


'''show_country() serves the page of a specific country. Template will
change if user is logged or not.'''


@app.route('/countries/<int:country_id>/')
def show_country(country_id):
    country = db_helper.get_country_by_id(country_id)
    attractions = db_helper.get_attractions(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None and country.user_id == \
            login_session['user_id']:
        return render_template('loggedcountry.html', country=country,
                               attractions=attractions)

    return render_template('country.html', country=country,
                           attractions=attractions)


'''country_json() returns all the information associated to a specific
country in a json format. '''


@app.route('/countries/<int:country_id>/json/')
def country_json(country_id):
    country = db_helper.get_country_by_id(country_id)
    attractions = db_helper.get_attractions(country_id)

    return jsonify(Country=country.serialize,
                   Attractions=[a.serialize for a in attractions])


'''edit_country() serves the page which lets the user edit a country. If
user is not logged, user will be redirected to homepage. '''


@app.route('/countries/<int:country_id>/edit/',
           methods=['GET', 'POST'])
def edit_country(country_id):
    country = db_helper.get_country_by_id(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is None or country.user_id != \
            login_session['user_id']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        db_helper.add_to_db(country)

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('editcountry.html', country=country)


'''delete_country() serves the page which lets the user remove a country. If
user is not logged, user will be redirected to homepage. '''


@app.route('/countries/<int:country_id>/delete/', methods=['GET', 'POST'])
def delete_country(country_id):
    country = db_helper.get_country_by_id(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is None or country.user_id != \
            login_session['user_id']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        db_helper.delete_attractions_by_country_id(country_id)
        db_helper.delete_from_database(country)

        return redirect(url_for('home'))

    return render_template('deletecountry.html', country=country)


'''new_country() serves the page which lets the user create a country. If
user is not logged, user will be redirected to homepage. '''


@app.route('/countries/new', methods=['GET', 'POST'])
def new_country():
    stored_access_token = login_session.get('access_token')
    if stored_access_token is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        inputs = request.form
        country = Country()
        country.user_id = login_session['user_id']

        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        db_helper.add_to_db(country)

        return redirect(url_for('home'))

    return render_template('newcountry.html')


'''show_attraction() serves the page of a specific attraction. Template will
change if user is looged or not. '''


@app.route('/countries/<int:country_id>/<int:attraction_id>/')
def show_attraction(country_id, attraction_id):
    country = db_helper.get_country_by_id(country_id)
    attraction = db_helper.get_attraction_by_id(attraction_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None and attraction.user_id == \
            login_session['user_id']:
        return render_template('loggedattraction.html', country=country,
                               attraction=attraction)

    return render_template('attraction.html', country=country,
                           attraction=attraction)


'''edit_attraction() serves the page which lets the user edit an attraction. If
user is not logged, user will be redirected to homepage. '''


@app.route('/countries/<int:country_id>/<int:attraction_id>/edit/',
           methods=['GET', 'POST'])
def edit_attraction(country_id, attraction_id):
    attraction = db_helper.get_attraction_by_id(attraction_id)
    country = db_helper.get_country_by_id(country_id)
    countries = db_helper.get_countries()

    stored_access_token = login_session.get('access_token')
    if stored_access_token is None or attraction.user_id != \
            login_session['user_id']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            attraction.name = inputs['name']
        if inputs['city']:
            attraction.city = inputs['city']
        if inputs['description']:
            attraction.description = inputs['description']

        db_helper.add_to_db(attraction)

        return redirect(url_for('show_attraction', country_id=country_id,
                                attraction_id=attraction_id))

    return render_template('editattraction.html', attraction=attraction,
                           country=country, countries=countries)


'''delete_attraction() serves the page which lets the user remove an
attraction. If user is not logged, user will be redirected to homepage. '''


@app.route('/countries/<int:country_id>/<int:attraction_id>/delete/',
           methods=['GET', 'POST'])
def delete_attraction(country_id, attraction_id):
    attraction = db_helper.get_attraction_by_id(attraction_id)
    country = db_helper.get_country_by_id(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is None or attraction.user_id != \
            login_session['user_id']:
        return redirect(url_for('home'))

    if request.method == 'POST':
        db_helper.delete_from_database(attraction)

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('deleteattraction.html', attraction=attraction,
                           country=country)


'''new_attraction() serves the page which lets the user create an
attraction. If user is not logged, user will be redirected to homepage. '''


@app.route('/countries/<int:country_id>/new/', methods=['GET', 'POST'])
def new_attraction(country_id):
    country = db_helper.get_country_by_id(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is None:
        return redirect(url_for('home'))

    if request.method == 'POST':
        inputs = request.form
        attraction = Attraction()
        attraction.user_id = login_session['user_id']

        if inputs['name']:
            attraction.name = inputs['name']
        if inputs['city']:
            attraction.city = inputs['city']
        if inputs['description']:
            attraction.description = inputs['description']

        attraction.country = country

        db_helper.add_to_db(attraction)

        return redirect(url_for('show_country', country_id=country_id))

    return render_template('newattraction.html', country=country)


'''create_user() is responsible for creating a new user and adding to
database. '''


def create_user(name, email):
    new_user = User(name=name, email=email)
    db_helper.add_to_db(new_user)

    user = db_helper.get_user_by_email(email)

    return user.id


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "my_name_is_goku"
    app.run(host='0.0.0.0', port=8000)
