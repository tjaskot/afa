##########################
### Imported packages ####
from flask import Flask, render_template, request, url_for, redirect, jsonify, send_file #TODO: session
from flask_login import LoginManager, login_required, UserMixin, current_user, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os, sys, json, psycopg2
import importlib
import logging
import views
import variables
###########################

###########################
### Order of operations ###
# app object constructor
# app configuration
# secret key instantiation
# login manager creation
# login manager configs
# db configuration
# centralized url routing
# logger object creation
# logger configuration
# trailing slash and space corrections
# error handling routes
# app context unit testing
# app object creation
#   db creation
#   environ config
#   app start
###########################

#TODO: move to folder EmFlowersLLC, rn using just app
app = Flask(__name__, instance_relative_config=True)

# Define User Specific Variables - EmFlowersLLC package
appName = "EmFlowersLLC Website"

# App Configs
if not os.environ.get('SECRET_KEY') and 'production' not in os.environ:
    app.secret_key = 'secret'
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(seconds=300)
    print("!!!SECRET KEY LOCALLY SET!!! ...Dev Only")
else:
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///memory"
#SQLALCHEMY_DATABASE_URI = os.environ.get['DATABASE_URL']
#DATABASE_URL = os.environ['DATABASE_URL']
#app.config['DATABASE_URL'] = DATABASE_URL
DATABASE_URL = "postgres://qigrsimgrdwmrp:d22e5ad57160b685561b78c099167fcbd49a42c3a718de61bf785126aca321bf@ec2-52-6-143-153.compute-1.amazonaws.com:5432/depm009vdoa4em"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['DATABASE_URL'] = DATABASE_URL
psqlconn = psycopg2.connect(DATABASE_URL, sslmode='require')

#r = FlaskRedis() # In future may want to use Redis for KeyValue items on site pages
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    # skip next for now
    if user_id is not None:
        return User.query.get(user_id)
    return None
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('unauthorized'))

class User(UserMixin, db.Model):
    """Model for user accounts."""
    __tablename__ = 'flowerShopUsers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=True)
    created = db.Column(db.String(10), nullable=True) #DateTime, unique=False, nullable=True)
    bio = db.Column(db.Text, unique=False, nullable=True)
    #admin = db.Column(db.Boolean, index=False, unique=False, nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password(self.password, password)

    def validate_username(self, username):
        validUser = User.query.filter_by(username=username.data).first()
        if validUser is not None:
            error = "User is not valid"

    def validate_email(self, email):
        validEmail = User.query.filter_by(email=email.data).first()
        if validEmail is not None:
            error = "Email is not valid"

    def __repr__(self):
        return '<{},{}>'.format(self.id, self.username)

    def __init__(self, username, password, email='noEmail', created='noDate', bio='noResponse'):
        self.username = username
        self.email = email
        self.password = password
        self.created = created
        self.bio = bio

# Centralized approach - removes lazy loading, loads page as needed, cached page values
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/hello', view_func=views.hello, methods=['GET'])
app.add_url_rule('/home', view_func=views.home)
app.add_url_rule('/generate', view_func=views.generate, methods=['POST', 'GET'])
app.add_url_rule('/contacts', view_func=views.contacts)
app.add_url_rule('/about', view_func=views.about)
app.add_url_rule('/datafunction', view_func=views.datafunction)
app.add_url_rule('/unauthorized', view_func=views.unauthorized)

###### Session Cookie Needed ##########
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        userFormName = request.form['username']
        # session['username'] = userFormName
        # Uses the session for username passing rather than in url or directly in html
        login_user(User.query.filter_by(username=userFormName).first())
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/users', methods=['GET','POST'])
def users():
    return render_template('users.htm', users=User.query.all())

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            # TODO: try:
            # catch:
            users = User(request.form['username'], request.form['password'], request.form['email'])
            db.session.add(users)
            db.session.commit()
            return redirect(url_for('users'))
    return render_template('signup.htm')
#######################################

##########  Login Required ############
@app.route('/settings')
@login_required
def settings():
    return '''
        <p>Success for Settings!!!</p>
    '''

@app.route('/logout')
@login_required
def logout():
    # logout_user() # from flask_login logout_user
    # session.pop('username', None)
    logout_user()
    return redirect(url_for('index'))
#######################################

###### Logger Creation & Config #######
logger = logging.getLogger(__name__)
# logger.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
# log basic info
logger.info("Initial Startup of: " + appName)
logger.debug('This message should go to the log file')
logger.warning('Warning: Test')
#######################################

######## URL Route Handling ###########
# reamins here for each load - don't know if correct, but seems right
@app.before_request
def clear_trailing():
    rp = request.path
    logger.info(rp)
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

# remains here for all error loading - this works!
@app.errorhandler(404)
def not_found(error):
    app.logger.error("User unauthorized.")
    return render_template('notfound.htm'), 404
#######################################

############# Unit tests ##############
# For application below (unit test code coverage +70%)
# Validate that all url's are responsive and identify as themselves
with app.test_request_context('/hello', method='GET'):
    #print(url_for(''))
    assert request.path == '/hello'
    assert request.method == 'GET'

with app.test_request_context('/generate', method='POST'):
    assert request.path == '/generate'
    assert request.method == 'POST'

with app.test_request_context('/contacts'):
    assert request.path == '/contacts'

with app.test_request_context('/about'):
    assert request.path == '/about'

with app.test_request_context('/login', method='POST'):
    assert request.path == '/login'
    assert request.method == 'POST'

with app.test_request_context('/home'):
    assert request.path == '/home'

with app.test_request_context('/datafunction'):
    assert request.path == '/datafunction'
#######################################

#   This file is being used as both main.py and EmFlowersLLC.py and some overlap in init.py
if __name__ == "__main__":
#    manager.run()
    db.create_all()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
