from flask import Blueprint
from flask import render_template, request, url_for, session as login_session
from werkzeug.utils import redirect

from db import dbhelper
from model.attraction import Attraction
from webservice.auth_gate import login_required

attraction_service = Blueprint(name='attraction', import_name=__name__)

db_helper = dbhelper.DbHelper()


@attraction_service.route('/countries/<int:country_id>/<int:attraction_id>/')
def show_attraction(country_id, attraction_id):
    """
    show_attraction() serves the page of a specific attraction.

    :param country_id: id of country
    :param attraction_id: id of attraction
    :return: attraction page template
    """

    country = db_helper.get_country_by_id(country_id)
    attraction = db_helper.get_attraction_by_id(attraction_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None and attraction.user_id == \
            login_session['user_id']:
        return render_template('loggedattraction.html', country=country,
                               attraction=attraction)

    return render_template('attraction.html', country=country,
                           attraction=attraction)


# @login_required
@attraction_service.route(
    '/countries/<int:country_id>/<int:attraction_id>/edit/',
    methods=['GET', 'POST'])
def edit_attraction(country_id, attraction_id):
    """
    edit_attraction() serves the page which lets the user edit an attraction.

    :param country_id: id of country
    :param attraction_id: id of attraction
    :return: edit attraction page template
    """

    attraction = db_helper.get_attraction_by_id(attraction_id)
    country = db_helper.get_country_by_id(country_id)
    countries = db_helper.get_countries()

    if attraction.user_id != login_session['user_id']:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            attraction.name = inputs['name']
        if inputs['city']:
            attraction.city = inputs['city']
        if inputs['description']:
            attraction.description = inputs['description']

        db_helper.add_to_db(attraction)

        return redirect(url_for('.show_attraction', country_id=country_id,
                                attraction_id=attraction_id))

    return render_template('editattraction.html', attraction=attraction,
                           country=country, countries=countries)


# @login_required
@attraction_service.route(
    '/countries/<int:country_id>/<int:attraction_id>/delete/',
    methods=['GET', 'POST'])
def delete_attraction(country_id, attraction_id):
    """
    delete_attraction() serves the page which lets the user remove an
    attraction.

    :param country_id: id of country
    :param attraction_id: id of attraction
    :return: delete attraction page template
    """

    attraction = db_helper.get_attraction_by_id(attraction_id)
    country = db_helper.get_country_by_id(country_id)

    if attraction.user_id != login_session['user_id']:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        db_helper.delete_from_database(attraction)

        return redirect(url_for('country.show_country', country_id=country_id))

    return render_template('deleteattraction.html', attraction=attraction,
                           country=country)


# @login_required
@attraction_service.route('/countries/<int:country_id>/new/',
                          methods=['GET', 'POST'])
def new_attraction(country_id):
    """
    new_attraction() serves the page which lets the user create an
    attraction.

    :param country_id:
    :return: new attraction page template
    """

    country = db_helper.get_country_by_id(country_id)

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

        return redirect(url_for('country.show_country', country_id=country_id))

    return render_template('newattraction.html', country=country)
