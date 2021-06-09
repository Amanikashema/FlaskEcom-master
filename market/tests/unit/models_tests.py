import unittest
from unittest import TestCase
from market.models import User, Item


class ModelsTests(unittest.TestCase):
    def test_user(self):
        user_info = User(id=1 , email_address='amanikashema@gmail.com', password_hash="kash123", username='Amani', budget=3)
        self.assertEqual(user_info.id, 1)
        self.assertEqual(user_info.email_address, 'amanikashema@gmail.com')
        self.assertEqual(user_info.password_hash, 'kash123')
        self.assertEqual(user_info.budget, 3)
        self.assertEqual(user_info.username, 'Amani')

    def test_items(self):
        test_info = Item(id=1,name='Amani',price=2000,barcode='12345',description='brown product',owner='23')
        self.assertEqual(test_info.id,1)
        self.assertEqual(test_info.name,'Amani')
        self.assertEqual(test_info.price,2000)
        self.assertEqual(test_info.barcode,'12345')
        self.assertEqual(test_info.description,'brown product')
        self.assertEqual(test_info.owner,'23')


if __name__ == '__main__':
    unittest.main()



