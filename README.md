user-service
============

- Because of the relatively constrained nature of the task I decided to use Flask and SQLite directly rather depend on an ORM or a framework like Flask-RESTful.
- I added an ID for users independent of the username they selected so we don't have to URL encode the usernames for the individual user end-point.
- I added a unique constraint on id and username since we're using autoincrement on the id.
- I added a logging warning to check whether the Flask SECRET_KEY has been set. Leaving a default there means the service can be run directly after checkout.  

TODO:
	- pydoc
	- limit and offset in responses