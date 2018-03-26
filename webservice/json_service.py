from flask import Blueprint, jsonify

from db import dbhelper

json_service = Blueprint(name='json', import_name=__name__)

db_helper = dbhelper.DbHelper()


@json_service.route('/countries/<int:country_id>/json/')
def country_json(country_id):
    """
    country_json() returns all the information associated to a specific
    country in a json format.

    :param country_id: id of country
    :return: string in json format
    """

    country = db_helper.get_country_by_id(country_id)
    attractions = db_helper.get_attractions(country_id)

    return jsonify(Country=country.serialize,
                   Attractions=[a.serialize for a in attractions])


@json_service.route('/attractions/<int:attraction_id>/json/')
def attraction_json(attraction_id):
    """
    attraction_json() returns all the information associated to a specific
    attraction in a json format.

    :param attraction_id: id of attraction
    :return: string in json format
    """

    attraction = db_helper.get_attraction_by_id(attraction_id)

    return jsonify(Attraction=attraction.serialize)
