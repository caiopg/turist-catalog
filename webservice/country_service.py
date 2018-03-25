from flask import Blueprint
from flask import render_template, request, url_for, session as login_session
from werkzeug.utils import redirect

from db import dbhelper
from model.country import Country
from webservice.auth_gate import login_required

country_service = Blueprint(name='country', import_name=__name__)

db_helper = dbhelper.DbHelper()


@country_service.route('/countries/<int:country_id>/')
def show_country(country_id):
    """
    show_country() serves the page of a specific country.

    :param country_id: id of the country
    :return: country page template
    """

    country = db_helper.get_country_by_id(country_id)
    attractions = db_helper.get_attractions(country_id)

    stored_access_token = login_session.get('access_token')
    if stored_access_token is not None and country.user_id == \
            login_session['user_id']:
        return render_template('loggedcountry.html', country=country,
                               attractions=attractions)

    return render_template('country.html', country=country,
                           attractions=attractions)


@login_required
@country_service.route('/countries/<int:country_id>/edit/',
                       methods=['GET', 'POST'])
def edit_country(country_id):
    """
    edit_country() serves the page which lets the user edit a country.

    :param country_id: id of country
    :return: edit country page template
    """

    country = db_helper.get_country_by_id(country_id)

    if country.user_id != login_session['user_id']:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        inputs = request.form
        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        db_helper.add_to_db(country)

        return redirect(url_for('country.show_country', country_id=country_id))

    return render_template('editcountry.html', country=country)


@login_required
@country_service.route('/countries/<int:country_id>/delete/',
                       methods=['GET', 'POST'])
def delete_country(country_id):
    """
    delete_country() serves the page which lets the user remove a country.

    :param country_id: id of country
    :return: remove country page template
    """

    country = db_helper.get_country_by_id(country_id)

    if country.user_id != login_session['user_id']:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        db_helper.delete_attractions_by_country_id(country_id)
        db_helper.delete_from_database(country)

        return redirect(url_for('home.home'))

    return render_template('deletecountry.html', country=country)


@login_required
@country_service.route('/countries/new', methods=['GET', 'POST'])
def new_country():
    """
    new_country() serves the page which lets the user create a country.

    :return: new country page template
    """

    if request.method == 'POST':
        inputs = request.form
        country = Country()
        country.user_id = login_session['user_id']

        if inputs['name']:
            country.name = inputs['name']
        if inputs['description']:
            country.description = inputs['description']

        db_helper.add_to_db(country)

        return redirect(url_for('home.home'))

    return render_template('newcountry.html')
