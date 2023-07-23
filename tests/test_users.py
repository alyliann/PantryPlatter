import unittest, sys, os

sys.path.append('../PantryPlatters') # imports python file from parent directory
from pantryplatters import app, db

class UsersTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def register(self, name, email, password):
        return self.app.post('/signup',
                            data=dict(name=name,
                                      email=email,
                                      password=password, 
                                      confirm_password=password),
                            follow_redirects=True)

    def test_valid_user_registration(self):
        response = self.register('test', 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_valid_email_registration(self):
        response = self.register('test2', 'test@example.com', 'FlaskIsAwesome')
        self.assertEqual(response.status_code, 200)

    def test_invalid_name_registration(self):
        response = self.register('t', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)
        response = self.register('thisIsMoreThan20Characters', 'test@example.com', 'FlaskIsAwesome')
        self.assertIn(b'Field must be between 2 and 20 characters long.', response.data)

    def test_invalid_email_registration(self):
        response = self.register('test2', 'test@example', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)
        response = self.register('test3', 'testexample.com', 'FlaskIsAwesome')
        self.assertIn(b'Invalid email address.', response.data)
    
    def test_invalid_password_registration(self):
        response = self.register('t', 'test@example.com', 'Flask')
        self.assertIn(b'Field must be at least 8 characters long.', response.data)

if __name__ == "__main__":
    unittest.main()
