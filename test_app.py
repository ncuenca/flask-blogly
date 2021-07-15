from unittest import TestCase
from app import app
from models import User, db

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyAppTestCase(TestCase):
    """Test Flask app for Blogly."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        User.query.delete()
        test_user = User(first_name="test", last_name="name", image_url="")   

        db.session.add(test_user)
        db.commit()

        self.test_user = test_user     

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

    # TODO: test something :)
    def test_homepage(self):
        """Make sure page is properly redirected."""

        with self.client as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 302)
    
    def test_user_info_page(self):
        """Make sure page is properly loaded with user info."""

        with self.client as client:
            response = client.get(f'/users/{self.test_user.id}')
            html = response.get_data(as_text=True)

            # TODO: test for user info
            self.assertIn('<button><a href="/users">Go Back</a></button>', html)
            self.assertEqual(response.status_code, 200)

