import os
import os.path

from flask import Flask, g, request, jsonify, abort
from flask.ext.bcrypt import Bcrypt

import users
from users import User, UserCreation
from db import DB, EntryAlreadyExists

app = Flask(__name__)
bcrypt = Bcrypt(app)

config_file = os.getenv('USER_SERVICE_SETTINGS', 'default_config.py')
app.config.from_pyfile(config_file)

if app.config['SECRET_KEY'] == 'insecure_default':
    app.logger.warn('Secret key set to default. Please change in configuration file (default config.py)')

@app.before_request
def before_request():
    db_file = app.config['DATABASE']
    g.db = DB(db_file, bcrypt)

@app.teardown_request
def after_request(err):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.errorhandler(400)
def bad_request(e):
    resp = jsonify({ 'message': str(e) })
    resp.status_code = 400
    return resp

@app.errorhandler(401)
def unauthorized(e):
    resp = jsonify({ 'message': str(e) })
    resp.status_code = 401
    return resp

@app.errorhandler(404)
def not_found(e):
    resp = jsonify({ 'message': str(e) })
    resp.status_code = 404
    return resp

if not app.config['DEBUG']:
    @app.errorhandler(Exception)
    def general_error(e):
        app.logger.exception(e)

        resp = jsonify({ 'message': str(e) })
        resp.status_code = 500
        return resp

@app.route('/users', methods = ['GET', 'POST'])
def users_endpoint():
    if request.method == 'POST':
        # Return BadRequest rather than InternalServerError if validation fails
        try:
            user_request = UserCreation(**request.json)
        except TypeError:
            return bad_request('Expected username, email and password. Got %s' % ', '.join(request.json.keys()))

        # Again return BadRequest if the user already exists, otherwise it is a genuine
        # error that we let the default error handlers deal with
        try:
            user_id = users.create_user(g.db, user_request)
        except EntryAlreadyExists:
            return bad_request('User %s already exists' % user_request.username)

        ret = User(user_id, user_request.username, user_request.email)._asdict()
        return jsonify(**ret)
    else:
        ret = {
            # jsonify renders named tuples without the field names
            # so we convert to a dictionary to ensure they are in the output
            'users': [user._asdict() for user in users.get_users(g.db)]
        }

        return jsonify(**ret)

@app.route('/users/<user_id>', methods = ['GET', 'DELETE'])
def user_endpoint(user_id):
    if request.method == 'DELETE':
        if request.headers.get('foobar') == app.config['VALID_API_KEY']:
            if users.get_user(g.db, user_id):
                users.delete_user(g.db, user_id)    
                return jsonify({ "message": "deleted" })
            else:
                abort(404)
        else:
            return unauthorized('Missing or invalid foobar API key header')
        
    else:
        user = users.get_user(g.db, user_id)
        if user:
            return jsonify(**user._asdict())
        else:
            abort(404)

def start():
    db_file = app.config['DATABASE']
    should_init_db_file = not os.path.isfile(db_file)

    # Make sure the DB file has been created and the schema SQL executed
    db = DB(db_file, bcrypt)
    
    if should_init_db_file:
        app.logger.info('Initialising %s with database schema' % db_file)
        users.init_db(db, app)

        if app.config['DEMO_USERS']:
            users.create_demo_users(db, app)

    db.close()

    app.run()

if __name__ == '__main__':
    start()