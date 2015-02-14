user-service
============

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

TODO:
	- pydoc
	- API docs

Test cases
	- Create users
	- List users
	- List user
	- Delete user

	- Create user with existing username
	- Create user with missing fields
	- List user that doesn't exist
	- Delete user that doesn't exist
	- Delete user without API key