# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# db = SQLAlchemy()
#
# def create_app():
#     app = Flask(__name__, instance_relative_config=False)
#
#     db.init_app(app)
#
#     with app.app_context():
#         from . import views  # Import routes
#         app.add_url_rule('/', view_func=views.index)
#         app.add_url_rule('/login', view_func=views.login, methods=['GET','POST'])
#         app.add_url_rule('/hello', view_func=views.hello, methods=['GET'])
#         app.add_url_rule('/home', view_func=views.home)
#         app.add_url_rule('/generate', view_func=views.generate, methods=['POST', 'GET'])
#         app.add_url_rule('/users', view_func=views.users)
#         app.add_url_rule('/signup', view_func=views.signup, methods=['GET','POST'])
#         app.add_url_rule('/contacts', view_func=views.contacts)
#         app.add_url_rule('/about', view_func=views.about)
#         app.add_url_rule('/datafunction', view_func=views.datafunction)
#         app.add_url_rule('/unauthorized', view_func=views.unauthorized)
#
#         db.create_all()  # Create database tables for our data models
#
#         return app
