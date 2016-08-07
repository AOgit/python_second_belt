""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):

        errors = []

        if not info['name']:
            errors.append('Name cannot be blank')
        elif len(info['name']) < 2:
            errors.append('Name must be at least 2 characters long')
        elif not info['name'].isalpha():
            errors.append("Name must be letters only.")
        if not info['username']:
            errors.append('Username cannot be blank')
        elif len(info['username']) < 3:
            errors.append('Username must be at least 3 characters long')
        elif not info['username'].isalpha():
            errors.append("Username must be letters only.")
        if not info['password']:
            errors.append('Password cannot be blank')
        elif len(info['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif info['password'] != info['p_con']:
            errors.append('Password and confirmation must match!')

        if errors:
            return {"status": False, "errors": errors}
        else:
            password = info['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (name, username, pw_hash) VALUES (:name, :username, :pw_hash)"
            data = {'name': info['name'], 'username': info['username'], 'pw_hash': hashed_pw}
            self.db.query_db(query, data)
            return {"status": True} 

    def login_user(self, info):
        password = info['password']
        user_query = "SELECT * FROM users WHERE username = :username LIMIT 1"
        user_data = {'username': info['username']}
        user = self.db.query_db(user_query, user_data)
        if user:
            if self.bcrypt.check_password_hash(user[0]['pw_hash'], password):
                return {'status': True, 'user': user[0]}
        return False

    def get_info(self, info):
        user_query = "SELECT * FROM users WHERE username = :username LIMIT 1"
        user_data = {'username': info['username']}
        return self.db.query_db(user_query, user_data) 

    """
    Below is an example of a model method that queries the database for all users in a fictitious application
    
    Every model has access to the "self.db.query_db" method which allows you to interact with the database

    def get_users(self):
        query = "SELECT * from users"
        return self.db.query_db(query)

    def get_user(self):
        query = "SELECT * from users where id = :id"
        data = {'id': 1}
        return self.db.get_one(query, data)

    def add_message(self):
        sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
        data = {'message': 'awesome bro', 'users_id': 1}
        self.db.query_db(sql, data)
        return True
    
    def grab_messages(self):
        query = "SELECT * from messages where users_id = :user_id"
        data = {'user_id':1}
        return self.db.query_db(query, data)

    """