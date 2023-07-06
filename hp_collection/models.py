from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash
import secrets
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    # creating our table and all the columns and setting them to their particular types
    id = db.Column(db.String, primary_key = True)
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = False, default = '')
    username = db.Column(db.String(150), nullable = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    character = db.relationship('Character', backref = 'owner', lazy = True)

    def __init__(self, email, username, password):     
        self.id = self.set_id()
        self.email = email
        self.username = username
        self.password = self.set_password(password)
        self.token = self.set_token()

    def set_id(self): 
        return str(uuid.uuid4())
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"User {self.username} has been added to the database!"
    
class Character(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(150), nullable = True)
    house = db.Column(db.String(30), nullable = True)
    nationality = db.Column(db.String(200), nullable = True)
    occupation = db.Column(db.String(100), nullable = True)
    books_appeared_in = db.Column(db.Integer, nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __init__(self, name, description, house, nationality, occupation, books_appeared_in, user_token):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.house = house
        self.nationality = nationality
        self.occupation = occupation
        self.books_appeared_in = books_appeared_in
        self.user_token = user_token

    def set_id(self):
        return str(uuid.uuid4())
    
    def __repr__(self):
        return f"'{self.name}' has been added to the database. Yay!"

class CharacterSchema(ma.Schema):
    class Meta:
        # these fields will come back from the API call
        fields = ['id', 'name', 'description', 'house', 'nationality', 'occupation', 'books_appeared_in']
        
character_schema = CharacterSchema()
characters_schema = CharacterSchema(many = True)   # will bring back a list of objects