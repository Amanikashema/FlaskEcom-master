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

    def test_password(self):
        password_variable = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3000)
        self.assertEqual(password_variable.password_hash,"kash123" )

    # password correctness test
    def test_password_correction(self):
        password = '123world'
        pw_hash = bcrypt.generate_password_hash(password)

        candidate = 'world'
        bcrypt.check_password_hash(pw_hash, candidate)
        self.assertFalse(bcrypt.check_password_hash(pw_hash, candidate))

    # Test if customer can buy products
    def test_purchase(self):
        item_info = Item(id=1, name='IPHONE', price=2000, barcode='12345', description='brown product', owner=23)
        purchase = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3000).can_purchase(item_info)
        self.assertTrue(purchase)

    # Test if item can be sold
    #def test_sell(self):
        item_info = Item(id=1, name='IPHONE', price=2000, barcode='12345', description='brown product', owner=1)
        purchase_info = User(id = 1, email_address='amanikashema@gmail.comu', password_hash="kash123", username='Amani',
                             budget=3000).can_sell(item_info)


        #self.assertIn(purchase_info.username,item_obj)
        #item_obj in self.items


    def test_buy(self):
        pass

    def test_sell(self):
        pass








