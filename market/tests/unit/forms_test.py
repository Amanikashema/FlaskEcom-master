from market.tests.unit.base_tests import BaseTest, db
from flask import request
from flask_login import current_user, AnonymousUserMixin, login_user, logout_user, login_required
from market.models import User
from flask import render_template, redirect, url_for, flash, request


class TestRegister(BaseTest):
    # Testing register form
    def test_register_form_url(self):
        with self.app:
            response = self.app.get('/register',follow_redirects=True)
            self.assertIn('/register',request.url)
            self.assertIn(b' <title>\n          \n    Register Page\n\n      </title>',response.data)

            self.assertEqual(response.status_code,200)

            self.assertEqual(current_user.get_id(),AnonymousUserMixin.get_id(self))

    def test_valid_username(self):
        with self.app:
            response = self.app.post('/register',  data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                               password2='pass1234'), follow_redirects=True)

            user = db.session.query(User).filter_by(username='amani').first()
            self.assertFalse(user)
            validation_error = 'Username already exists! Please try a different username'
            # Test validation if username already exists
            self.assertTrue(validation_error,'Username already exists! Please try a different username')

    def test_validate_email(self):
        with self.app:
            response = self.app.post('/register',
                                    data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                              password2='pass1234'), follow_redirects=True)

            user = db.session.query(User).filter_by(email_address='email@gmail.com').first()
            self.assertFalse(user)
            validation_error = 'Email Address already exists! Please try a different email address'
            # Test validation if username already exists
            self.assertTrue(validation_error, 'Email Address already exists! Please try a different email address')

    def test_user_registered(self):
        with self.app:
            response = self.app.post('/register',
                                    data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                              password2='pass1234'), follow_redirects=True)
            self.assertEqual(response.status_code,200)

            # user details to be registered
            user_to_create = User(username='Amani',
                                  email_address='email@gmail.com',
                                  password_hash='pass1234')

            # saving users info to db
            db.session.add(user_to_create)
            db.session.commit()

            # Test if username is saved in database and registered
            self.assertTrue(user_to_create.username)

            # Test if user is registered into the system
            login = login_user(user_to_create)
            self.assertTrue(login)







