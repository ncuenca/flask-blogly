from unittest import TestCase
from app import app
from models import User, db, Post

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_testdb'
app.config['SQLALCHEMY_ECHO'] = False




class BloglyAppTestCase(TestCase):
    """Test Flask app for Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        db.drop_all() #seperate this out
        db.create_all() 

        self.client = app.test_client()
        app.config['TESTING'] = True

        User.query.delete()
        test_user = User(first_name="test", last_name="name", image_url="")

        Post.query.delete()
        test_post = Post(title="test", content="test", user_id=test_user.id)

        db.session.add_all([test_user, test_post])
        db.session.commit()

        self.test_user = test_user
        self.test_post = test_post

    def test_homepage(self):
        """Make sure page is properly redirected."""

        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)

    def test_users_page(self):
        """Users page is loaded and accessed."""

        with self.client as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Users Template.', html)

    def test_delete_user_post(self):
        """Make sure page is properly redirected after user deleted."""

        with self.client as client:
            response = client.post(f'/users/{self.test_user.id}/delete')
            # should be testing on models.py as well

            self.assertEqual(response.status_code, 302)

    def test_user_info_page(self):
        """Make sure page is properly loaded with user info."""

        with self.client as client:
            response = client.get(f'/users/{self.test_user.id}')
            html = response.get_data(as_text=True)

            self.assertIn(
                f'<h1>{self.test_user.first_name} {self.test_user.last_name}</h1>', html)
            self.assertEqual(response.status_code, 200)

            # make a new method testing failed response
            response_failed = client.get('/users/0')
            self.assertEqual(response_failed.status_code, 404)

    def test_show_post(self):
        """Make sure post page is properly loaded with post info."""

        with self.client as client:
            response = client.get(f'/posts/{self.test_post.id}')
            html = response.get_data(as_text=True)
            
            self.assertIn(
                f'<h1>{self.test_post.title}</h1>', html)
            self.assertEqual(response.status_code, 200)

            response_failed = client.get('/posts/0')
            self.assertEqual(response_failed.status_code, 404)

    def test_new_post_page(self):
        """Make sure new post creation page is working"""

        with self.client as client:
            response = client.get(f'/users/{self.test_user.id}/posts/new')
            html = response.get_data(as_text=True)

            self.assertIn(
                f'<h1>Add Post for {self.test_user.first_name} {self.test_user.last_name}</h1>', html)
            self.assertEqual(response.status_code, 200)

    def test_edited_post(self):
        """Make sure post gets edited and updated in database"""

        with self.client as client:

            response = client.post(f'/posts/{self.test_post.id}/edit',
                                   data={"title": "Hi", "content": "Hello"})

            self.assertEqual(response.status_code, 302)
