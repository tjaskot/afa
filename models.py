# from flask_login import UserMixin
# from flask_sqlalchemy import SQLAlchemy
#
# class User(UserMixin, db.Model):
#     """Model for user accounts."""
#     __tablename__ = 'flowerShopUsers'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=True, nullable=False)
#     password = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(80), nullable=True)
#     created = db.Column(db.String(10), nullable=True) #DateTime, unique=False, nullable=True)
#     bio = db.Column(db.Text, unique=False, nullable=True)
#     #admin = db.Column(db.Boolean, index=False, unique=False, nullable=True)
#
#     def set_password(self, password):
#         self.password = generate_password_hash(password, method='sha256')
#
#     def check_password(self, password):
#         return check_password(self.password, password)
#
#     def validate_username(self, username):
#         validUser = User.query.filter_by(username=username.data).first()
#         if validUser is not None:
#             error = "User is not valid"
#
#     def validate_email(self, email):
#         validEmail = User.query.filter_by(email=email.data).first()
#         if validEmail is not None:
#             error = "Email is not valid"
#
#     def __repr__(self):
#         return '<{},{}>'.format(self.id, self.username)
#
#     def __init__(self, username, password, email='noEmail', created='noDate', bio='noResponse'):
#         self.username = username
#         self.email = email
#         self.password = password
#         self.created = created
#         self.bio = bio
