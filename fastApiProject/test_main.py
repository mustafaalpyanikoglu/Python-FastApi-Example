from fastapi.testclient import TestClient
from fastapi import status

from .main import app

client = TestClient(app)

def test_read_item():
	response = client.get("/items/foo", headers={"X-Token": "conneofsilence"})
	assert response.status_code == status.HTTP_200_OK
	assert response.json() == {
		"id": "foo",
		"title": "Foo",
		"description": "There goes my hero",
	}