from datetime import datetime
from appdir import db
from werkzeug.security import check_password_hash, generate_password_hash
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # relationship
    recipes = db.relationship('Recipe', back_populates='author', lazy='dynamic')
    sub_sorts = db.relationship('SubSort', back_populates='author', lazy='dynamic')
    comments = db.relationship('Comment', back_populates='author', lazy='dynamic')

    # The hash encryption of password and email confirming token studies the instruction in Book
    # "FLASK Web Development: Developing Web Applications with Python, Second Edition"
    @property
    def password(self):
        raise AttributeError('password is not readable')

    # encrypting the password set by user
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # deciphering the encrypted password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # return one readable string to represent the model, helping test
    def __repr__(self):
        return '<User %r>' % self.user_name


class Sort(db.Model):
    __tablename__ = 'sorts'
    id = db.Column(db.Integer, primary_key=True)
    sort_name = db.Column(db.String(64), unique=True, index=True)
    # relationship
    sub_sorts = db.relationship('SubSort', back_populates='sort', lazy='dynamic')


recipeSorts = db.Table('recipeSorts',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipes.id')),
    db.Column('sort_id', db.Integer, db.ForeignKey('subsorts.id')),
)


class SubSort(db.Model):
    __tablename__ = 'subsorts'
    id = db.Column(db.Integer, primary_key=True)
    sub_sort_name = db.Column(db.String(64), unique=True, index=True)
    # foreign keys:
    # each sub-sort should be dependent to a typical big sort, created by a user
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sort_id = db.Column(db.Integer, db.ForeignKey('sorts.id'))
    # relationship
    author = db.relationship('User', back_populates='sub_sorts', lazy='joined')
    sort = db.relationship('Sort', back_populates='sub_sorts', lazy='joined')
    # recipes = db.relationship('Recipe', back_populates='sort', lazy='dynamic')


class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(64), nullable=False, index=True)
    recipe_description = db.Column(db.String(258))
    recipe_step_list = db.Column(db.String(128))
    recipe_image_route = db.Column(db.String(64))
    # foreign keys:
    # each recipe should be dependent to a typical sort, posted by a user
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # sort_id = db.Column(db.Integer, db.ForeignKey('subsorts.id'))
    # relationship
    author = db.relationship('User', back_populates='recipes', lazy='joined')
    # sort = db.relationship('SubSort', back_populates='recipes', lazy='joined')
    comments = db.relationship('Comment', back_populates='recipe', lazy='dynamic')
    sorts = db.relationship('SubSort',
                            secondary=recipeSorts,
                            backref=db.backref('recipes', lazy='dynamic'),
                            lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(), nullable=False)
    # foreign keys:
    # each comment should be dependent to a typical recipe, posted by a user
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'))
    #
    author = db.relationship('User', back_populates='comments', lazy='joined')
    recipe = db.relationship('Recipe', back_populates='comments', lazy='joined')


