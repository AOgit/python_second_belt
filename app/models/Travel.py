""" 
    Sample Model File

    A Model should be in charge of communicating with the Database. 
    Define specific model method that query the database for information.
    Then call upon these model method in your controller.

    Create a model using this template.
"""
from system.core.model import Model
import time

class Travel(Model):
    def __init__(self):
        super(Travel, self).__init__()

    def show_all_travels(self, id):
        query = "SELECT users.name, plans.id as product, plans.destination, plans.start_date, plans.end_date, plans.plan FROM plans LEFT JOIN my_plan ON plans.id = my_plan.plan_id LEFT JOIN users ON plans.user_id = users.id WHERE my_plan.user_id <> :id ^ my_plan.user_id is null AND plans.user_id <> :id"
        data = {'id':id}
        return self.db.query_db(query, data)

    def show_my_travels(self, id):
        query = "SELECT plans.id as product, plans.destination, plans.start_date, plans.end_date, plans.plan FROM plans LEFT JOIN my_plan ON my_plan.plan_id = plans.id LEFT JOIN users ON plans.user_id = users.id WHERE plans.user_id = :id OR my_plan.user_id = :id"
        data = {'id':id}
        return self.db.query_db(query, data)

    def add_travel(self, info):
        errors = []
        current_date = time.strftime("%Y-%m-%d")

        if not info['destination']:
            errors.append('Destination cannot be blank')
        if not info['plan']:
            errors.append('Description cannot be blank')
        if info['start_date'] < current_date:
            errors.append('Travel dates only apply in the future')
        if info['end_date'] < info['start_date']:
            errors.append('Travel Date To must not be before Travel Date From')
        
        if errors:
            return {'status': False, 'errors': errors}
        else:
            query = "INSERT INTO plans (user_id, destination, plan, start_date, end_date) VALUES (:user_id, :destination, :plan, :start_date, :end_date)"
            data = {'user_id': info['id'], 'destination': info['destination'], 'plan': info['plan'], 'start_date': info['start_date'], 'end_date': info['end_date']}
            self.db.query_db(query, data)
            return {'status': True}

    def add_to_trip(self, info):
        query = "INSERT INTO my_plan (user_id, plan_id) VALUES (:user_id, :plan_id)"
        data = {'user_id': info['user'], 'plan_id': info['product']}
        return self.db.query_db(query, data)

    def get_dest_profile(self, id):
        query = "SELECT * FROM plans LEFT JOIN users ON plans.user_id = users.id WHERE plans.id = :id"
        data = {'id': id}
        return self.db.query_db(query, data)

    def get_people_coming(self, info):
        query = "SELECT name FROM users LEFT JOIN my_plan ON users.id = my_plan.user_id WHERE my_plan.plan_id = :id"
        data = {'id': info['id']}
        return self.db.query_db(query, data)

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