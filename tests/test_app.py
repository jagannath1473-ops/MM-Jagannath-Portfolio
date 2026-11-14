import sqlite3
import tempfile
import unittest
from pathlib import Path

from app import create_app


class PortfolioAppTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_directory.name) / "test.db"
        self.app = create_app(
            {
                "TESTING": True,
                "DATABASE_PATH": str(self.database_path),
                "DATABASE_URL": "",
            }
        )
        self.client = self.app.test_client()

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_homepage_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"M M Jagannath", response.data)
        self.assertIn(b"CareerCompass", response.data)

    def test_health_endpoint(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok", "storage": "sqlite"})

    def test_contact_submission_is_saved(self):
        response = self.client.post(
            "/api/contact",
            json={
                "name": "Test Visitor",
                "email": "visitor@example.com",
                "message": "This is a complete test message.",
            },
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.get_json()["ok"])

        connection = sqlite3.connect(self.database_path)
        row = connection.execute(
            "SELECT name, email, message FROM contact_messages"
        ).fetchone()
        connection.close()
        self.assertEqual(
            row,
            ("Test Visitor", "visitor@example.com", "This is a complete test message."),
        )

    def test_contact_validation(self):
        test_cases = [
            ({"name": "J", "email": "valid@example.com", "message": "Long enough message"}, "name"),
            ({"name": "Jagannath", "email": "not-an-email", "message": "Long enough message"}, "email"),
            ({"name": "Jagannath", "email": "valid@example.com", "message": "short"}, "message"),
        ]
        for payload, field in test_cases:
            with self.subTest(field=field):
                response = self.client.post("/api/contact", json=payload)
                self.assertEqual(response.status_code, 400)
                body = response.get_json()
                self.assertFalse(body["ok"])
                self.assertIn(field, body["errors"])

    def test_contact_rejects_non_json(self):
        response = self.client.post("/api/contact", data="plain text")
        self.assertEqual(response.status_code, 415)


if __name__ == "__main__":
    unittest.main()
