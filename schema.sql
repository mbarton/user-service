drop table if exists users;

create table users (
	id text primary key,
	username text not null,
	email text not null,
	password text not null
);

create unique index user_index on users(username);