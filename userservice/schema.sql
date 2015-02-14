drop table if exists users;

create table users (
	id integer primary key autoincrement,
	username text,
	email text not null,
	password text not null
);

create unique index user_index on users(id, username);