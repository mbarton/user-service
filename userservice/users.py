from collections import namedtuple

User = namedtuple('User', 'id, username, email')

def get_users(db):
	users = db.read_all('select id, username, email from users', {})
	return map(User._make, users)

def get_user(db, user_id):
	results = db.read_all('select id, username, email from users where id = :user_id', { 'user_id': user_id })
	if len(results) > 0:
		return User._make(results[0])
	else:
		return None

def create_user(db, username, email, password):
	hashed_password = db.secure_hash(password)
	params = { 'username': username, 'email': email, 'password': hashed_password }
	db.write('insert into users values(NULL, :username, :email, :password)', params)
