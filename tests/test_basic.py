import unittest, sys

sys.path.append('../PantryPlatters') # imports python file from parent directory
from pantryplatters import app # imports flask app object

class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()

    def test_home_page(self):
        response_1 = self.app.get('/', follow_redirects=True)
        response_2 = self.app.get('/home', follow_redirects=True)
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
    
    def test_my_recipes_page(self):
        response = self.app.get('/my_recipes', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_recipe_finder_page(self):
        response = self.app.get('/recipe_finder', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    
    def test_signup_page(self):
        response = self.app.get('/signup', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()