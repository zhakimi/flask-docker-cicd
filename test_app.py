"""Pytest suite for the Flask service — run by CI on every push."""

import pytest

from app import APP_NAME, create_app


@pytest.fixture()
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_index_returns_ok_and_lists_endpoints(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["app"] == APP_NAME
    assert "/health" in data["endpoints"]


def test_health_reports_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"


def test_info_exposes_app_and_version(client):
    resp = client.get("/api/info")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["app"] == APP_NAME
    assert "version" in data


def test_unknown_route_is_404(client):
    assert client.get("/nope").status_code == 404
