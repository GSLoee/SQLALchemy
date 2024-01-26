"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
    
    def greet(self):
        return f"{self.first_name} {self.last_name}"