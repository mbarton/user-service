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

def delete_user(db, user_id):
    db.execute('delete from users where id = :id', { 'id': user_id })

#############################################################

def create_demo_users(db, app):
    demo_users = ['user%s' % n for n in range(0, 10)]
    app.logger.info('Initialising demo users: %s' % ", ".join(demo_users))
    for user in demo_users:
        email = '%s@email.com' % user
        create_user(db, UserCreation(user, email, user))

def init_db(db, app):
    with app.open_resource('schema.sql', mode='r') as schema_file:
        db.unsafe_execute_block(schema_file.read())