drop table if exists users;
create table users (
	username text primary key,
	email text not null,
	password text not null
);