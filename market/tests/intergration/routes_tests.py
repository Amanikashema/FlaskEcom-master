from market.tests.unit.base_tests import BaseTest, db
from flask import request
from market.models import User, Item
from market import routes


class TestRoutes(BaseTest):
    def test_home_route(self):
        with self.app:
            response = self.app.get('/home', follow_redirects=True)
            # tests status code from home page
            self.assertEqual(response.status_code, 200)

    # function to test if user can buy item with enough money
    def test_market_route_enough_money(self):
        with self.app:
            response1 = self.app.post('/register',
                                      data=dict(email_address='email@gmail.com', username='amani',
                                                password1='pass1234',
                                                password2='pass1234'), follow_redirects=True)

            item_info = Item(id=1, name='phone', price=2000, barcode='12345', description='brown product', owner='1')
            db.session.add(item_info)
            db.session.commit()
            user = db.session.query(User).filter_by(username='amani').first()
            user.budget = 5000
            db.session.commit()
            # check if user budget is 5000
            self.assertEqual(user.budget, 5000)
            # Make sure that item is in db
            result = db.session.query(Item).filter_by(name='phone').first()
            self.assertTrue(result)
            response = self.app.post('/market', data=dict(purchased_item='phone'), follow_redirects=True)
            # tests status code of market page
            self.assertEqual(response.status_code, 200)
            # test to buy item when user has enough money
            self.assertIn(b'Congratulations! You purchased phone for 2000$', response.data)

    # function to test if user can buy with not enough money
    def test_market_route_not_enough_money(self):
        with self.app:
            response1 = self.app.post('/register',
                                      data=dict(email_address='email@gmail.com', username='amani',
                                                password1='pass1234',
                                                password2='pass1234'), follow_redirects=True)

            item_info = Item(id=1, name='phone', price=2000, barcode='12345', description='brown product', owner='1')
            db.session.add(item_info)
            db.session.commit()
            user = db.session.query(User).filter_by(username='amani').first()
            user.budget = 1000
            db.session.commit()
            # check if user budget is 1000
            self.assertEqual(user.budget, 1000)
            # Make sure that item is in db
            result = db.session.query(Item).filter_by(name='phone').first()
            self.assertTrue(result)
            response = self.app.post('/market', data=dict(purchased_item='phone'), follow_redirects=True)
            # tests status code of market page
            self.assertEqual(response.status_code, 200)
            # test to buy item when user don't have enough money
            self.assertIn(b"Unfortunately, you don&#39;t have enough money to purchase phone!", response.data)

    def test_market_route_sell_item_owner(self):
        with self.app:

            # create user
            response1 = self.app.post('/register',
                                      data=dict(email_address='email@gmail.com', username='amani',
                                                password1='pass1234',
                                                password2='pass1234'), follow_redirects=True)

            # create item and save to db
            item_info = Item(id=1, name='phone', price=2000, barcode='12345', description='brown product', owner=' 1')
            db.session.add(item_info)
            db.session.commit()

            # assert user owns item
            user = db.session.query(User).filter_by(username='amani').first()
            self.assertEqual(user.username,'amani')

            self.assertTrue(user.items,'phone')

            # sell item with post req

            response = self.app.post('/market',data=dict(sold_item='phone'), follow_redirects=True)
            self.assertIn(b'Congratulations!',response.data)


    def test_market_route_sell_item_non_owner(self):
        with self.app:
            # create user
            response1 = self.app.post('/register',
                                      data=dict(email_address='email@gmail.com', username='amani',
                                                password1='pass1234',
                                                password2='pass1234'), follow_redirects=True)

            # create item and save to db
            item_info = Item(id=1, name='phone', price=2000, barcode='12345', description='brown product')
            db.session.add(item_info)
            db.session.commit()

            # assert user owns item
            user = db.session.query(User).filter_by(username='amani').first()
            self.assertEqual(user.username, 'amani')

            self.assertEqual(user.items, [])

            # sell item with post req if user does not own product

            response = self.app.post('/market', data=dict(sold_item='phone'), follow_redirects=True)
            self.assertIn(b'Something went wrong', response.data)

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
