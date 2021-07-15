"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """Redirect to list of users."""

    return redirect('/users')

@app.route('/users')
def users_page():
    """Show all users.
       Make these links to view the detail page for the user.
       Have a link here to the new-user form."""

    users = User.query.order_by('last_name').all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def new_user():
    """Show an add form for users."""

    return render_template('new_user.html')

@app.route('/users/new', methods=['POST'])
def new_user_post():
    """Process the add form, adding a new user and going back to /users."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["img-url"] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Show information about the given user.
       Have a button to get to their edit page, and to delete the user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template('user_info.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user.
       Have a cancel button that returns to the detail page for a user, and 
       a save button that updates the user."""
    
    user = User.query.get_or_404(user_id)

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_post(user_id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get_or_404(user_id)

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["img-url"]
    
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_post(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def new_post_page(user_id):
    """Direct to the page for creating new post"""

    user = User.query.get_or_404(user_id)


    return render_template('new_post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def create_post(user_id):
    """Create a new post and update database"""

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user.id)
    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{user.id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post.
       Show buttons to edit and delete the post."""
    
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    
    return render_template('post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit')
def edit_post_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""
    
    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edited_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)

    title = request.form["title"]
    content = request.form["content"]
    
    post.title = title
    post.content= content

    db.session.commit()    

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def tags_page():
    '''Lists all tags, with links to the tag detail page.'''

    tags = Tag.query.all()

    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_page(tag_id):
    '''Show detail about a tag. Have links to edit form and to delete.'''
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_info.html', tag=tag)

@app.route('/tags/new')
def create_tag_page():
    '''Shows a form to add a new tag.'''
    
    return render_template('new_tag.html')

@app.route('/tags/new', methods=['POST'])
def post_new_tag():
    '''Process add form, adds tag, and redirect to tag list.'''

    tag = Tag(name=request.form['tag-name'])
    db.session.add(tag)
    db.session.commit()
    
    return redirect('/tags') 

@app.route('/tags/<int:tag_id>/edit')
def edit_tag_page(tag_id):
    '''Show edit form for a tag'''
    
    tag = Tag.query.get_or_404(tag_id)

    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def post_tag_edit(tag_id):
    '''Process edit form, edit tag, and redirects to the tags list.'''
    
    tag = Tag.query.get_or_404(tag_id)

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    '''Process edit form, edit tag, and redirects to the tags list.'''
    
    tag = Tag.query.get_or_404(tag_id)

    return redirect('/tags')