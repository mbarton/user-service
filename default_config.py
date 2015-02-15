DATABASE = '/tmp/user-service.db'
DEBUG = True
SECRET_KEY = "insecure_default"

# Generate example users when initialising the database
DEMO_USERS = True

# User deletions must include this value as the `foobar` header
VALID_API_KEY = "1234"