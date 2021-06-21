from market.forms import RegisterForm
from market.tests.unit.base_tests import BaseTest, db
from flask import request
from flask_login import current_user, AnonymousUserMixin, login_user, logout_user, login_required
from market.models import User
from flask import render_template, redirect, url_for, flash, request
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError


class TestRegister(BaseTest):
    # Testing register form Url
    def test_register_form_url(self):
        with self.app:
            response = self.app.get('/register',
                                    data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                              password2='pass1234'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(request.url, 'http://localhost/register')

    def test_username_already_exist(self):
        with self.app:
            with self.app_context:
                response1 = self.app.post('/register',
                                          data=dict(username="amani", email_address="email@gmail.com",
                                                    password1="pass1234", password2="pass1234", ), follow_redirects=True)

                user = db.session.query(User).filter_by(email_address="email@gmail.com").first()
                self.assertTrue(user)

                class Username():
                    data = "amani"

                with self.assertRaises(ValidationError) as context:
                    RegisterForm().validate_username(Username)
                    self.assertEqual('Username already exists! Please try a different username', str(context.exception))

    def test_email_already_exists(self):
        with self.app:
            with self.app_context:
                response1 = self.app.post('/register',
                                         data=dict(username="amani", email_address="email@gmail.com",
                                                   password1="password1234", password2="password1234",), follow_redirects=True)

                user = db.session.query(User).filter_by(email_address="email@gmail.com").first()
                self.assertTrue(user)

                class Email:
                    data = "email@gmail.com"

                with self.assertRaises(ValidationError) as context:
                    RegisterForm().validate_email_address(Email)
                    self.assertEqual('Email Address already exists! Please try a different email address', str(context.exception))

    def test_user_registered(self):
        with self.app:
            response = self.app.post('/register',
                                     data=dict(email_address='email@gmail.com', username='amani', password1='pass1234',
                                               password2='pass1234'), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # test that user is created
            self.assertIn(b'Account created successfully! You are now logged in as amani', response.data)
