user-service
============

Quick Start
-----------

**Installing dependencies**:

	pip install -r requirements.txt

- I used a `virtualenv` as well: https://virtualenv.pypa.io/en/latest/userguide.html#usage

**Running the app**:

	python app.py

- The database is created in `/tmp/user-service.db` and populated with some example users
- App configuration is listed in `default_config.py`.
- Point the environment variable `USER_SERVICE_SETTINGS` to your own copy of `default_config.py` to change configuration.

**Running the tests**:

	python tests.py

**Building the documentation**:

	cd doc; make html

- Sphinx must be installed (it is not in requirements.txt since it is only required for docs)
- `pip install sphinx`
- In addition, the Sphinx HTTP doc extension is required:
- `pip install sphinxcontrib-httpdomain`
- *GitHub unfortunately does not render the docs properly so it must be done manually*

Design Notes
------------

- Because of the relatively constrained nature of the task I decided to use Flask and SQLite directly rather depend on an ORM or a framework like Flask-RESTful or Flask-Restless.

- I added an UUID for users independent of the username they selected
	- The id is the primary key and there is a unique index on username
	- This gives us flexibility in the future in case we want to support changing usernames

- I added a logging warning to check whether the Flask SECRET_KEY has been set. Leaving a default there means the service can be run directly after checkout. 

- I haven't validated the format of email addresses
	- I'd really want a framework to do this properly since it is notoriously difficult
	- Django has an email form validator

- I haven't added pagination to the /users endpoint so it could potentially return a lot of information
	- To do this I'd add offset and limit query parameters
	- Default: offset=0, limit=100
	- I also now see that the spec says there's no need for reading multiple users at once. I'm leaving the end-point anyway for now.