"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session 
from models import db, connect_db, User, Post, PostTag, Tag 

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
    # post = Post.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)
    return render_template('post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    user = User.query.get_or_404(user_id)
    # post = Post.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']
    tags_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()
    new_post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(new_post)
    db.session.commit()   

    return redirect(f"/{user.id}") 

@app.route('/users/<int:user_id>/posts/<int:post_id>')
def view_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', user=user, post=post, tags=tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def update_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('update_post.html',user=user, post=post, tags=tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=["POST"])
def edit_post(user_id, post_id):
    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)
    
    post.title = request.form['title']
    post.content = request.form['content']

    tags_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()
    post.tags = tags

    db.session.commit()   

    return redirect(f"/users/{user.id}/posts/{post.id}")


@app.route('/tags')
def view_tags():
    tags = Tag.query.all()
    return render_template('tags_list.html', tags=tags)

@app.route('/tags/new')
def add_tag_form():
    return render_template('add_tag.html')

@app.route('/tags/new', methods=["POST"])
def add_tag():
    name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=name, posts=posts)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route(f'/tags/<int:tag_id>')
def view_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    user = User.query.all()
    post = Post.query.all()

    return render_template('view_tag.html', tag=tag, user=user, post=post)

@app.route(f'/tags/<int:tag_id>/edit')
def edit_tag_html(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route(f'/tags/<int:tag_id>/edit', methods=['POST'])
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag.id}')

@app.route(f'/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')