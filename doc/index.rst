Welcome to User Service's documentation!
========================================

A simple JSON web service for creating, reading and deleting users.

In addition to their username, the users email address is also stored.

Passwords are stored as bcrypt hashes. Data are stored in a SQLite file.

.. http:get:: /users
    
    List the stored users.

    **Example response**:

    .. sourcecode:: http

        {
          "users": [
            {
              "email": "user0@email.com", 
              "id": "df1b7afe-9449-48f2-a384-414e5b1d9537", 
              "username": "user0"
            }, 
            {
              "email": "user1@email.com", 
              "id": "9876da3c-615c-4a2e-bc05-605596f2dcf2", 
              "username": "user1"
            }, 
            {
              "email": "user2@email.com", 
              "id": "723c07b0-b29c-4166-9c89-cec4e7e264b0", 
              "username": "user2"
            }, 
            {
              "email": "user3@email.com", 
              "id": "59e4ea98-111b-4364-896a-068f50d91f75", 
              "username": "user3"
            }
        }

.. http:post:: /users
    
    Create a new user.

    Once created, the ID of the new user is returned.

    **Example request**:

    .. sourcecode:: http

        {
            "username": "mtest",
            "email": "mtest@internet.com",
            "password": "1234"
        }

    **Example response**:

    .. sourcecode:: http

        {
            "id": "0d9953f3-2513-4b86-b928-5bb9f110b1c5",
            "username": "mtest"
            "email": "mtest@internet.com"
        }

    :statuscode 200: the user was created sucessfully
    :statuscode 400: the username or password are already in use

.. http:get:: /users/:id

    Get information about a user with a given ID.

    **Example request**:

    .. sourcecode:: http

        GET http://localhost/users/df1b7afe-9449-48f2-a384-414e5b1d9537

    **Example response**:

    .. sourcecode:: http

        {
            "id": "df1b7afe-9449-48f2-a384-414e5b1d9537", 
            "username": "user0"
            "email": "user0@email.com", 
        }

    :statuscode 200: information about the user was returned sucessfully
    :statuscode 404: the user with the given ID could not be found

.. http:delete:: /users/:id

    Deletes a user with a given ID.

    The request must be authorised by passing your API key as the ``foobar`` header.

    **Example request**:

    .. sourcecode:: http

        DELETE http://localhost/users/df1b7afe-9449-48f2-a384-414e5b1d9537
        foobar: my_api_key_value

    **Example response**:

    .. sourcecode:: http

        {
            "message": "deleted"
        }  

    :statuscode 200: the user was deleted successfully
    :statuscode 401: the ``foobar`` API key was missing or incorrect
    :statuscode 404: the user with the given ID could not be found