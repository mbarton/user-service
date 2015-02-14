import os
import os.path

from flask import Flask, g, request, jsonify, abort
from flask.ext.bcrypt import Bcrypt

from db import DB, EntryAlreadyExists
from users import create_user, get_users, get_user, User, UserCreation

app = Flask(__name__)
bcrypt = Bcrypt(app)

config_file = os.getenv('USER_SERVICE_SETTINGS', 'default_config.py')
app.config.from_pyfile(config_file)

if app.config['SECRET_KEY'] == 'insecure_default':
    app.logger.warn('Secret key set to default. Please change in configuration file (default config.py)')

db_file = app.config['DATABASE']

@app.before_request
def before_request():
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

@app.route('/users', methods = ['GET', 'POST'])
def users():
    if request.method == 'POST':
        # Return BadRequest rather than InternalServerError if validation fails
        try:
            user_request = UserCreation(**request.json)
        except TypeError:
            return bad_request('Expected username, email and password. Got %s' % ', '.join(request.json.keys()))

        # Again return BadRequest if the user already exists, otherwise it is a genuine
        # error that we let the default error handlers deal with
        try:
            user_id = create_user(g.db, user_request)
        except EntryAlreadyExists:
            return bad_request('User %s already exists' % user_request.username)

        ret = {
            'user': User(user_id, user_request.username, user_request.email)._asdict()
        }

        return jsonify(**ret)
    else:
        ret = {
            # jsonfiy renders named tuples without the field names
            # so we convert to a dictionary to ensure they are in the output
            'users': [user._asdict() for user in get_users(g.db)]
        }

        return jsonify(**ret)

@app.route('/users/<user_id>', methods = ['GET', 'DELETE'])
def user(user_id):
    if request.method == 'DELETE':
        pass
    else:
        user = get_user(g.db, user_id)
        if user:
            return jsonify(**user._asdict())
        else:
            abort(404)

def create_demo_users(db):
    demo_users = ['user%s' % n for n in range(0, 10)]
    app.logger.info('Initialising demo users: %s' % ", ".join(demo_users))
    for user in demo_users:
        email = '%s@email.com' % user
        create_user(db, UserCreation(user, email, user))

def start():
    should_init_db_file = not os.path.isfile(db_file)

    # Make sure the DB file has been created and the schema SQL executed
    db = DB(db_file, bcrypt)
    
    if should_init_db_file:
        app.logger.info('Initialising %s with database schema' % db_file)

        with app.open_resource('schema.sql', mode='r') as schema_file:
            db.unsafe_execute_block(schema_file.read())
    
        if app.config['DEMO_USERS']:
            create_demo_users(db)

    db.close()

    app.run()