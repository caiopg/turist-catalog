from functools import wraps

from flask import url_for, session as login_session, has_request_context
from werkzeug.utils import redirect


def login_required(input_func):
    @wraps(input_func)
    def wrapper():
        if has_request_context():
            stored_access_token = login_session.get('access_token')
            if stored_access_token is None:
                return redirect(url_for('home.home'))
            else:
                input_func()
    return wrapper()
