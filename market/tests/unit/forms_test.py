from market.tests.unit.base_tests import BaseTest, db
from flask import request
from flask_login import current_user, AnonymousUserMixin, login_user, logout_user, login_required
from market.models import User
from flask import render_template, redirect, url_for, flash, request


class TestRegister(BaseTest):
    # Testing register form Url
    def test_register_form_url(self):
        with self.app:
            response = self.app.get('/register', data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                               password2='pass1234'),follow_redirects=True)
            self.assertEqual(response.status_code,200)
            self.assertIn(request.url,'http://localhost/register')


    def test_valid_username(self):
        with self.app:
            response = self.app.post('/register',  data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                               password2='pass1234'), follow_redirects=True)

            user = db.session.query(User).filter_by(username='amani').first()

            # chek if user is in database
            self.assertTrue(user)
            validation_error = 'Username already exists! Please try a different username'
            # Test validation if username already exists
            self.assertTrue(validation_error,'Username already exists! Please try a different username')

    def test_validate_email(self):
        with self.app:
            self.app.post('/register',
                                    data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                              password2='pass1234'), follow_redirects=True)

            user = db.session.query(User).filter_by(email_address='email@gmail.com').first()

            # chek if email is in database
            self.assertTrue(user)

            validation_error = 'Email Address already exists! Please try a different email address'
            # Test validation if username already exists
            self.assertTrue(validation_error, 'Email Address already exists! Please try a different email address')

    def test_user_registered(self):
        with self.app:
            response = self.app.post('/register',
                                    data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                              password2='pass1234'), follow_redirects=True)
            self.assertEqual(response.status_code,200)
            # test that user is created
            self.assertIn(b'Account created successfully! You are now logged in as amani', response.data)







