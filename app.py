"""Blogly application."""

from flask import Flask, redirect, render_template
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
    return redirect('/users')

@app.route('/users/<int:user_id>')
def get_user(user_id):
    """Show information about the given user.
       Have a button to get to their edit page, and to delete the user."""
    return render_template('user_info.html', user=user_id)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """Show the edit page for a user.
       Have a cancel button that returns to the detail page for a user, and 
       a save button that updates the user."""
    return render_template('edit_user.html', user=user_id)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user_post(user_id):
    """Process the edit form, returning the user to the /users page."""
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_post(user_id):
    """Delete the user."""
    return redirect('/users')