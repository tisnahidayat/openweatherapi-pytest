
import pytest, json
from utils.api_client import APIClient

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

def test_setup(api_client):
    response = api_client.get("data/2.5/weather", params={"q": "London"})
    assert response["cod"] == 200
    assert "weather" in response
    assert "main" in response
    assert "wind" in response
    assert "name" in response
    assert response["name"] == "London"
    print("Test pertama berhasil dijalankan dengan sukses!")
    print("Response:", json.dumps(response, indent=3))

