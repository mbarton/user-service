import uuid
from collections import namedtuple

User = namedtuple('User', 'id, username, email')
UserCreation = namedtuple('UserCreation', 'username, email, password')

def get_users(db):
    users = db.read_all('select id, username, email from users', {})
    return map(User._make, users)

def get_user(db, user_id):
    results = db.read_all('select id, username, email from users where id = :user_id', { 'user_id': user_id })
    if len(results) > 0:
        return User._make(results[0])
    else:
        return None

def create_user(db, req):
    user_id = str(uuid.uuid4())
    hashed_password = db.secure_hash(req.password)
    params = { 'id': user_id, 'username': req.username, 'email': req.email, 'password': hashed_password }
    
    db.write('insert into users values(:id, :username, :email, :password)', params)

    return user_id
