user-service
============

- Because of the relatively constrained nature of the task I decided to use Flask and SQLite directly rather depend on an ORM or a framework like Flask-RESTful.
- I set the `user` field as the primary key of the table since the brief doesn't require changing usernames once created and this enforces uniqueness.
- My go-to alternatives should such a feature be required would be to use an AUTO INCREMENT id column or generate a UUID for each user and set the primary key to both columns. For example:

	create table users (
		id integer autoincrement,
		username text not null,
		email text not null,
		password text not null,
		primary key (id, username)
	);

or

	create table users (
		id text not null,
		username text not null,
		email text not null,
		password text not null,
		primary key (id, username)
	);

- I added a logging warning to check whether the Flask SECRET_KEY has been set. Leaving a default there means the service can be run directly after checkout.  

TODO:
	- pydoc