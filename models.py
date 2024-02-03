"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
def connect_db(app):
    db.app = app 
    db.init_app(app)

DEFAULT_IMG = "https://t4.ftcdn.net/jpg/00/64/67/27/360_F_64672736_U5kpdGs9keUll8CRQ3p3YaEv2M6qkVY5.jpg"
class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        u = self 
        return f"<User id={u.id} first name={u.first_name} last name ={u.last_name}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    
    first_name = db.Column(db.String(50),
                            nullable=False)

    last_name = db.Column(db.String(50), 
                            nullable=False)

    image_url = db.Column(db.Text, 
                            nullable=False, 
                            default=DEFAULT_IMG)
    
    posts = db.relationship("Post", backref="users")

    def first(self):
        return f"{self.first_name}"
    
    def last(self):
        return f"{self.last_name}"
    
    def image(self):
        return f"{self.image_url}"
    
    def greet(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ ="posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)    

    def post_title(self):
        return f"{self.title}"
    
    def post_content(self):
        return f"{self.content}"

    def post_time(self): 
        return f"{self.created_at}"

class PostTag(db.Model):
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')
    
    def tag_name(self):
        return f"{self.name}"