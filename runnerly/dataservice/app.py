import os
from werkzeug.exceptions import HTTPException
from flakon import create_app as _create_app
from flakon.util import error_handling
from flask import request, abort, g
from flask_cors import CORS

import jwt

from .views import blueprints
from .database import db


_HERE = os.path.dirname(__file__)
os.environ['TESTDIR'] = os.path.join(_HERE, 'tests')
_SETTINGS = os.path.join(_HERE, 'settings.ini')


def create_app(settings=None):
    if settings is None:
        settings = _SETTINGS

    app = _create_app(blueprints=blueprints, settings=settings)

    with open(app.config['pub_key']) as f:
        app.config['pub_key'] = f.read()

    CORS(app)

    @app.before_request
    def before_req():
        if app.config.get('NEED_TOKEN', True):
            authenticate(app, request)

    return app


def _400(desc):
    exc = HTTPException()
    exc.code = 400
    exc.description = desc
    return error_handling(exc)


def authenticate(app, request):
    key = request.headers.get('Authorization')
    if key is None:
        return abort(401)

    key = key.split(' ')
    if len(key) != 2:
        return abort(401)

    if key[0].lower() != 'bearer':
        return abort(401)

    pub_key = app.config['pub_key']
    try:
        token = key[1]
        token = jwt.decode(token, pub_key, audience='runnerly.io')
    except Exception as e:
        return abort(401)

    # we have the token ~ copied into the globals
    g.jwt_token = token
