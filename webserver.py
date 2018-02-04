from flask import Flask, render_template, request, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import redirect

from db_setup import Base, DB_PATH, Country, Attraction

app = Flask(__name__)

engine = create_engine(DB_PATH)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/countries/')
def home():
    countries = session.query(Country)

    return render_template('home.html', countries=countries)


@app.route('/countries/<int:country_id>/')
def show_country(country_id):
    country = session.query(Country).filter_by(id=country_id).one()
    attractions = session.query(Attraction).filter_by(
        country_id=country_id).all()

    return render_template('country.html', country=country,
                           attractions=attractions)


@app.route('/countries/<int:country_id>/edit', methods=['GET', 'POST'])
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


@app.route('/countries/<int:country_id>/<int:attraction_id>/')
def show_attraction(country_id, attraction_id):
    country = session.query(Country).filter_by(id=country_id).one()
    attraction = session.query(Attraction).filter_by(id=attraction_id).one()

    return render_template('attraction.html', country=country,
                           attraction=attraction)


@app.route('/countries/<int:country_id>/<int:attraction_id>/edit',
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


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
