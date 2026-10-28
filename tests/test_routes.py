"""
Test Cases for Account Service
"""
import unittest
import json
from service import app, db
from service.models import Account

BASE_URL = "/accounts"

ACCOUNT_DATA = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "address": "123 Main St",
    "phone_number": "555-1234",
    "date_joined": "2023-01-01",
}


class TestAccountService(unittest.TestCase):
    """Account Service Test Cases"""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.drop_all()

    def setUp(self):
        with app.app_context():
            db.session.query(Account).delete()
            db.session.commit()

    def _create_account(self, data=None):
        data = data or ACCOUNT_DATA
        return self.client.post(
            BASE_URL,
            data=json.dumps(data),
            content_type="application/json",
        )

    def test_health(self):
        """Test health endpoint"""
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)

    def test_create_account(self):
        """Test CREATE an account"""
        resp = self._create_account()
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data["name"], ACCOUNT_DATA["name"])
        self.assertEqual(data["email"], ACCOUNT_DATA["email"])

    def test_list_accounts(self):
        """Test LIST all accounts"""
        self._create_account()
        self._create_account({"name": "Jane Doe", "email": "jane@example.com"})
        resp = self.client.get(BASE_URL)
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(len(data), 2)

    def test_read_account(self):
        """Test READ a single account"""
        create_resp = self._create_account()
        account_id = create_resp.get_json()["id"]
        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertEqual(data["name"], ACCOUNT_DATA["name"])

    def test_read_account_not_found(self):
        """Test READ account that does not exist"""
        resp = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(resp.status_code, 404)

    def test_update_account(self):
        """Test UPDATE an account"""
        create_resp = self._create_account()
        account_id = create_resp.get_json()["id"]
        updated = {**ACCOUNT_DATA, "name": "Updated Name"}
        resp = self.client.put(
            f"{BASE_URL}/{account_id}",
            data=json.dumps(updated),
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["name"], "Updated Name")

    def test_delete_account(self):
        """Test DELETE an account"""
        create_resp = self._create_account()
        account_id = create_resp.get_json()["id"]
        resp = self.client.delete(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get(f"{BASE_URL}/{account_id}")
        self.assertEqual(resp.status_code, 404)

    def test_security_headers(self):
        """Test that security headers are present"""
        resp = self.client.get("/health")
        self.assertIn("X-Content-Type-Options", resp.headers)

    def test_cors_headers(self):
        """Test CORS headers are present"""
        resp = self.client.get(BASE_URL)
        self.assertIn("Access-Control-Allow-Origin", resp.headers)


if __name__ == "__main__":
    unittest.main()
