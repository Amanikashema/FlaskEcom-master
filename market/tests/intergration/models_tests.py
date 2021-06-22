import unittest
from market.models import User, Item
from market.tests.unit.base_tests import BaseTest, db
from market import bcrypt


# class to test CRUD
class TestModelsCrud(BaseTest):
    def test_user_models_crud(self):
        with self.app_context:

            # Create new User
            new_user = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3000)

            # Assert that this User does not exist in db
            results = db.session.query(User).filter_by(username="Amani").first()
            self.assertIsNone(results)

            # save to db
            db.session.add(new_user)
            db.session.commit()

            # Delete from db
            db.session.delete(new_user)
            db.session.commit()

            # Assert it no longer exist in db
            results = db.session.query(User).filter_by(username="Amani").first()
            self.assertIsNone(results)

    def test_item_models_crud(self):
        with self.app_context:
            # Create new Items
            items = Item(id=1,name='IPHONE',price=2000,barcode='12345',description='brown product',owner='23')

            # Assert that this Item does not exist in db
            results = db.session.query(Item).filter_by(name="IPHONE").first()
            self.assertIsNone(results)

            # save to db
            db.session.add(items)
            db.session.commit()

            # Delete from db
            db.session.delete(items)
            db.session.commit()

            # Assert it no longer exist in db
            results = db.session.query(Item).filter_by(name="IPHONE").first()
            self.assertIsNone(results)


class TestProperties(BaseTest):
    # Function to test prettier budget
    def test_prettier_budget(self):
        budget_variable = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3000)
        self.assertEqual(budget_variable.prettier_budget, '3,000$')

    # function to test password
    def test_password(self):
        user = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3000)
        password = user.password
        self.assertEqual(password, user.password_hash)

    # function to test password setter
    def test_password_setter(self):
        with self.app_context:
            self.app.post('/register', data=dict(
                username='steve', email_address='okays@gmail.com',
                password1='password', password2='password'), follow_redirects=True)
            user = db.session.query(User).filter_by(username='steve').first()
            self.assertNotEqual(user.password, 'password')
            print(user.password)

    # password correctness test
    def test_password_correction(self):
        with self.app_context:
            self.app.post('/register', data=dict(
                username='steves', email_address='okayss@gmail.com',
                password1='password', password2='password'), follow_redirects=True)
            user = db.session.query(User).filter_by(username='steves').first()
            # self.assertEqual(user)

            password_hash = User.check_password_correction(user, 'password')
            self.assertTrue(password_hash)

            # Logging in with an incorrect password
            password_hash1 = User.check_password_correction(user, "passwords")
            self.assertFalse(password_hash1)

    # Test buy method
    def test_item_buy_method(self):
        with self.app_context:
            response = self.app.post('/register', data=dict(
                username='amani', email_address='email@gmail.com',
                password1='password1234', password2='password1234'), follow_redirects=True)
            user = db.session.query(User).filter_by(username='amani').first()
            user.budget = 1500
            self.assertTrue(user)

            item = Item(id=1, name="phone", price=1000, barcode=123457, description="covers", owner=1)
            db.session.add(item)
            db.session.commit()

            items = db.session.query(Item).filter_by(name="phone").first()

            items.buy(user)
            self.assertTrue(items)

            self.assertEqual(user.budget, 3000)
            self.assertEqual(item.owner, 1)

            item.sell(user)
            self.assertEqual(user.budget, 3000)
            self.assertEqual(item.owner, None)

    # test item repr method function
    def test_item_repr_method(self):
        item = Item(name='Phone', price=2000, barcode='testing', description='Model')

        new_item = item.__repr__()

        self.assertEqual(new_item, 'Item Phone')

    # function to test item sell method
    def test_item_sell_method(self):
        user = User(id=1, username='amani', email_address='email@gmail.com', password_hash='password1234', budget=5000)

        item = Item(name='Phone', price=2000, barcode='testing', description='Model', owner=1)

        can_sell = item.sell(user)

        db.session.commit()

        self.assertIsNone(can_sell)











