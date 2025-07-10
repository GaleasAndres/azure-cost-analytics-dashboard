import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from app import app

client = app.test_client()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

