import sys
import os

sys.path.insert(
    0,
    os.path.abspath("app")
)

from main import app


def test_home():

    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200

    assert b"Hello from Jenkins CI/CD" in response.data


def test_health():

    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json["status"] == "UP"