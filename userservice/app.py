import os
import os.path
from flask import Flask, g
from .db import DB

app = Flask(__name__)

config_file = os.getenv('USER_SERVICE_SETTINGS', 'default_config.py')
app.config.from_pyfile(config_file)

if app.config['SECRET_KEY'] == 'insecure_default':
    app.logger.warn('Secret key set to default. Please change in configuration file (default config.py)')

db_file = app.config['DATABASE']

@app.before_request
def before_request():
    g.db = DB(db_file)

@app.teardown_request
def after_request(err):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def start():
    should_init_db_file = not os.path.isfile(db_file)

    # Make sure the DB file has been created and the schema SQL executed
    db = DB(db_file)
    
    if should_init_db_file:
        with app.open_resource('schema.sql', mode='r') as schema_sql:
            db.execute_block(schema_sql)
    
    db.close()

    app.run()