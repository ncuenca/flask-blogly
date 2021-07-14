"""Blogly application."""

from flask import Flask, redirect, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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
def user_page():
    """Show all users.
       Make these links to view the detail page for the user.
       Have a link here to the new-user form."""
    users = User.query.all()
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
    image_url = request.form["img-url"]

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Show information about the given user.
       Have a button to get to their edit page, and to delete the user."""

    user = User.query.get(user_id)

    return render_template('user_info.html', user_id=user_id, user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user.
       Have a cancel button that returns to the detail page for a user, and 
       a save button that updates the user."""
    
    user = User.query.get(user_id)

    return render_template('edit_user.html', user_id=user_id, user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_post(user_id):
    """Process the edit form, returning the user to the /users page."""

    user = User.query.get(user_id)
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

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')