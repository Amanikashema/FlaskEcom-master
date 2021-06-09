import unittest
from market.models import User, Item
from market.tests.unit.base_tests import BaseTest, db


# class to test CRUD
class TestModelsCrud(BaseTest):
    def test_models_crud(self):
        with self.app_context:

            # Create new User
            new_user = User(email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3)

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





