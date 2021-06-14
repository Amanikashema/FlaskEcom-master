from market.tests.unit.base_tests import BaseTest, db
from flask import request
from market.models import User


class TestRoutes(BaseTest):
    def test_home_route(self):
        with self.app:
            response = self.app.get('/home', follow_redirects=True)
            # tests status code from home page
            self.assertEqual(response.status_code, 200)

    def test_market_route(self):
        with self.app:

            self.app.post('/register',
                          data=dict(email_address='email@gmail.com', username='amani',
                                    password1='pass1234',
                                    password2='pass1234'), follow_redirects=True)

            self.app.post('/login',
                                          data=dict(email_address='email@gmail.com', username='amani',
                                                    password='pass1234',
                                                    ), follow_redirects=True)
            response = self.app.post('/market', follow_redirects=True)
            # tests status code of market page
            self.assertEqual(response.status_code, 200)

            print(response.data)
            print(request.url)

    # function to test return success message
    def test_register_route_valid(self):
        with self.app:
            response = self.app.get('/register', follow_redirects=True)
            # tests status code of register page
            self.assertEqual(response.status_code, 200)
            self.assertIn(request.url, 'http://localhost/register')

            response_post = self.app.post('/register',
                                          data=dict(email_address='email@gmail.com', username='amani',
                                                    password1='pass1234',
                                                    password2='pass1234'), follow_redirects=True)
            # print(response_post.data)
            self.assertEqual(response_post.status_code, 200)
            # test if account was created
            self.assertIn(b"Account created successfully! You are now logged in as amani", response_post.data)

    # function to test if request returns error message with invalid details
    def test_register_route_invalid(self):
        with self.app:
            response_post = self.app.post('/register',
                                          data=dict(email_address='email@gmail.com', username='amani',
                                                    password1='pass124',
                                                    password2='pass1234'), follow_redirects=True)
            # print(response_post.data)
            self.assertEqual(response_post.status_code, 200)
            # test if account was created
            self.assertIn(b"There was an error with creating a user:", response_post.data)

    def test_login_valid(self):
        with self.app:
            response = self.app.get('/login', follow_redirects=True)
            # tests status code of login page
            self.assertEqual(response.status_code, 200)
            # test if returns login url
            self.assertIn(request.url, 'http://localhost/login')

            self.app.post('/register',
                          data=dict(email_address='email@gmail.com', username='amani',
                                    password1='pass1234',
                                    password2='pass1234'), follow_redirects=True)

            response_post = self.app.post('/login',
                                          data=dict(email_address='email@gmail.com', username='amani',
                                                    password='pass1234',
                                                    ), follow_redirects=True)

            self.assertIn(b'Success! You are logged in as: amani', response_post.data)

    def test_login_invalid(self):
        with self.app:
            self.app.post('/register',
                          data=dict(email_address='email@gmail.com', username='amani',
                                    password1='pass1234',
                                    password2='pass1234'), follow_redirects=True)

            response_post = self.app.post('/login',
                                          data=dict(email_address='email@gmail.com', username='amani',
                                                    password='pass123',
                                                    ), follow_redirects=True)

            self.assertIn(b'Username and password are not match! Please try again', response_post.data)

    def test_log_out(self):
        with self.app:
            response = self.app.get('/logout', data=dict(email_address='email@gmail.com', username='amani',
                                    password1='pass1234',
                                    password2='pass1234'), follow_redirects=True)
            # tests status code of logout page
            self.assertEqual(response.status_code, 200)
            self.assertIn(request.url, 'http://localhost/home')
            self.assertIn(b'You have been logged out!', response.data)