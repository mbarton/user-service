drop table if exists users;

create table users (
	id text primary key,
	username text not null,
	email text not null,
	password text not null
);

create unique index username_index on users(username);
create unique index email_index on users(email);