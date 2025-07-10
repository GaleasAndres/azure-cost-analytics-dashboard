from app import app

client = app.test_client()


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, World!"}
