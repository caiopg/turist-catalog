from flask import Flask

from webservice.attraction_service import attraction_service
from webservice.country_service import country_service
from webservice.google_service import google_service
from webservice.home_service import home_service
from webservice.json_service import json_service

"""
This class is responsible for initiating Flask. It is also responsible
for retrieving the correct html pages, populating them with the correct
elements and serving the browser.
"""

app = Flask(__name__)


if __name__ == '__main__':
    app.debug = True
    app.secret_key = "my_name_is_goku"

    app.register_blueprint(attraction_service)
    app.register_blueprint(country_service)
    app.register_blueprint(google_service)
    app.register_blueprint(home_service)
    app.register_blueprint(json_service)

    app.run(host='0.0.0.0', port=8000)
