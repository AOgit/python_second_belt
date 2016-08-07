"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Travels(Controller):
    def __init__(self, action):
        super(Travels, self).__init__(action)
        """
        This is an example of loading a model.
        Every controller has access to the load_model method.
        """
        self.load_model('User')
        self.load_model('Travel')
        self.db = self._app.db

        """
        
        This is an example of a controller method that will load a view for the client 

        """
   
    def index(self):
        """
        A loaded model is accessible through the models attribute 
        self.models['WelcomeModel'].get_users()
        
        self.models['WelcomeModel'].add_message()
        # messages = self.models['WelcomeModel'].grab_messages()
        # user = self.models['WelcomeModel'].get_user()
        # to pass information on to a view it's the same as it was with Flask
        
        # return self.load_view('index.html', messages=messages, user=user)
        """
        return self.load_view('index.html')

    def create(self):
        user_info = {
            'name': request.form['name'],
            'username': request.form['username'],
            'password': request.form['password'],
            'p_con': request.form['p_con']
        }

        create_status = self.models['User'].create_user(user_info)
        
        if create_status['status'] == True:
            flash('Success!! You may now log in.')
            return redirect('/')
        else:
            for message in create_status['errors']:
                flash(message)
            return redirect('/')           

    def login(self):
        user_info = {
            'username': request.form['username'],
            'password': request.form['password']
        }

        login_status = self.models['User'].login_user(user_info)

        if login_status['status'] == True:
            session['id'] = login_status['user']['id']
            session['username'] = login_status['user']['username']
            return redirect('/home')
        else:
            flash('Access denied')
            return redirect('/')

    def show(self):
        my_travels = self.models['Travel'].show_my_travels(session['id'])
        other_travel = self.models['Travel'].show_all_travels(session['id'])
        username = {
            'username': session['username']
        }
        name = self.models['User'].get_info(username)
        return self.load_view('dashboard.html', name=name[0]['name'], my_travels=my_travels, other_travel=other_travel)

    def add_travel_view(self):
        return self.load_view('add_travel.html')

    def add_new_travel(self):

        create_travel = self.models['Travel'].add_travel(request.form)

        if create_travel['status'] == True:
            return redirect('/home')
        else:
            for message in create_travel['errors']:
                flash(message)
            return redirect('/add_travel_view')

    def add_to_trip(self, id):
        info = {'product': id, 'user': session['id']}
        self.models['Travel'].add_to_trip(info)
        return redirect('/home')

    def get_travel_profile(self, id):
        this_dest = self.models['Travel'].get_dest_profile(id)
        extra = {
            'id': id,
            'user': session['id']
        }
        peoples = self.models['Travel'].get_people_coming(extra)
        return self.load_view('destination.html', this_dest=this_dest, peoples=peoples)

    def logout(self):
        session.clear()
        return redirect('/')
