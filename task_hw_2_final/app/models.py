from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id:int):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(100))
    last_Name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    image_file = db.Column(db.String(20), nullable=False, default='default-user.png')
    books = db.relationship('Book', backref='book_owner', lazy='dynamic')
    journals = db.relationship('Journal', backref='journal_owner', lazy='dynamic')
    def __repr__(self):
        return f'<User [username={self.username}, email={self.email}]>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.now)
    title = db.Column(db.String(150))
    author = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    image_file = db.Column(db.String(20), nullable=False, default='default-book.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, index=True, default=datetime.now)
    title = db.Column(db.String(150))
    editor = db.Column(db.String(200))
    page_amount = db.Column(db.Integer)
    image_file = db.Column(db.String(20), nullable=False, default='default-journal.png')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
