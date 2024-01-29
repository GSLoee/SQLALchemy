"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretthings'

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new')
def users_form():

    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/')

@app.route('/<int:user_id>')
def get_user(user_id):
    post = User.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user, post=post)


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route('/users/<int:user_id>/posts/new')
def new_post(user_id):
    post = User.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)
    return render_template('post.html', user=user, post=post)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def edit_post(user_id):
    post = User.query.get_or_404(user_id)
    user = Post.query.get_or_404(user_id)
    user.title = request.form['title'],
    user.content = request.form['content']
                
    db.session.add(user)
    db.session.commit()   

    return redirect(f"/{user.id}") 

