"""A minimal Flask service demonstrating a containerized CI/CD workflow.

Three endpoints: a landing route, a health check (used by the Docker
HEALTHCHECK and by orchestrators), and a small info API. The app factory
pattern keeps the app importable by tests and by gunicorn alike.
"""

import os
from datetime import datetime, timezone

from flask import Flask, jsonify

APP_NAME = "flask-docker-cicd"
VERSION = os.environ.get("APP_VERSION", "1.0.0")


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/")
    def index():
        return jsonify(
            message="Hello from a containerized Flask app!",
            app=APP_NAME,
            endpoints=["/", "/health", "/api/info"],
        )

    @app.get("/health")
    def health():
        return jsonify(status="ok", time=datetime.now(timezone.utc).isoformat())

    @app.get("/api/info")
    def info():
        return jsonify(
            app=APP_NAME,
            version=VERSION,
            environment=os.environ.get("FLASK_ENV", "production"),
        )

    return app


app = create_app()

if __name__ == "__main__":
    # development server only; the container runs gunicorn instead
    app.run(host="0.0.0.0", port=8000, debug=True)
