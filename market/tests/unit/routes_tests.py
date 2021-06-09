from market.tests.unit.base_tests import BaseTest


class TestRoutes(BaseTest):
    def test_home_route(self):
        with self.app:
            response = self.app.get('/home', follow_redirects=True)
            # tests status code from home page
            self.assertEqual(response.status_code, 200)

    def test_market_route(self):
        with self.app:
            response = self.app.get('/market', follow_redirects=True)
            # tests status code of market page
            self.assertEqual(response.status_code, 200)

    def test_register_route(self):
        with self.app:
            response = self.app.get('/register', follow_redirects=True)
            # tests status code of register page
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        with self.app:
            response = self.app.get('/login', follow_redirects=True)
            # tests status code of login page
            self.assertEqual(response.status_code, 200)

    def test_log_out(self):
        with self.app:
            response = self.app.get('/logout', follow_redirects=True)
            # tests status code of logout page
            self.assertEqual(response.status_code, 200)



