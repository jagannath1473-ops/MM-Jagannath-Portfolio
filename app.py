"""Flask application for M M Jagannath's personal portfolio."""

from __future__ import annotations

import os
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from flask import Flask, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATABASE_PATH = BASE_DIR / "instance" / "portfolio_messages.db"
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=os.environ.get("DATABASE_PATH", str(DEFAULT_DATABASE_PATH)),
        DATABASE_URL=os.environ.get("DATABASE_URL", ""),
        JSON_SORT_KEYS=False,
        MAX_CONTENT_LENGTH=32 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    initialize_database(app)

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify(status="ok", storage=storage_kind(app))

    @app.post("/api/contact")
    def contact():
        if not request.is_json:
            return jsonify(ok=False, message="Please submit the form as JSON."), 415

        payload = request.get_json(silent=True) or {}
        name = str(payload.get("name", "")).strip()
        email = str(payload.get("email", "")).strip().lower()
        message = str(payload.get("message", "")).strip()

        errors: dict[str, str] = {}
        if len(name) < 2:
            errors["name"] = "Please enter at least 2 characters."
        elif len(name) > 80:
            errors["name"] = "Name must be 80 characters or fewer."

        if not EMAIL_PATTERN.fullmatch(email):
            errors["email"] = "Please enter a valid email address."
        elif len(email) > 254:
            errors["email"] = "Email address is too long."

        if len(message) < 10:
            errors["message"] = "Please enter at least 10 characters."
        elif len(message) > 2000:
            errors["message"] = "Message must be 2,000 characters or fewer."

        if errors:
            return (
                jsonify(
                    ok=False,
                    message="Please correct the highlighted fields.",
                    errors=errors,
                ),
                400,
            )

        try:
            store_message(app, name=name, email=email, message=message)
        except Exception:
            app.logger.exception("Contact message could not be stored")
            return (
                jsonify(
                    ok=False,
                    message="Your message could not be saved. Please try again.",
                ),
                500,
            )

        return (
            jsonify(
                ok=True,
                message="Thanks! Your message has been saved successfully.",
            ),
            201,
        )

    @app.errorhandler(413)
    def payload_too_large(_error):
        return jsonify(ok=False, message="The submitted message is too large."), 413

    return app


def storage_kind(app: Flask) -> str:
    return "postgresql" if app.config.get("DATABASE_URL") else "sqlite"


@contextmanager
def sqlite_connection(app: Flask) -> Iterator[sqlite3.Connection]:
    path = Path(app.config["DATABASE_PATH"])
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def initialize_database(app: Flask) -> None:
    if app.config.get("DATABASE_URL"):
        import psycopg

        with psycopg.connect(app.config["DATABASE_URL"]) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS contact_messages (
                        id BIGSERIAL PRIMARY KEY,
                        name VARCHAR(80) NOT NULL,
                        email VARCHAR(254) NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
        return

    with sqlite_connection(app) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def store_message(app: Flask, *, name: str, email: str, message: str) -> None:
    if app.config.get("DATABASE_URL"):
        import psycopg

        with psycopg.connect(app.config["DATABASE_URL"]) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO contact_messages (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message),
                )
        return

    with sqlite_connection(app) as connection:
        connection.execute(
            "INSERT INTO contact_messages (name, email, message) VALUES (?, ?, ?)",
            (name, email, message),
        )


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
