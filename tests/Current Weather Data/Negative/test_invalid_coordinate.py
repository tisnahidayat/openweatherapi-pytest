
import pytest, json
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.mark.negative
def test_invalid_coordinate(api_client):

    response = api_client.get("data/2.5/weather", params={"lat": 999.999 , "lon": 999.999}) # Example of invalid coordinates

    assert response.status_code == 400, "Response status code should be 400 for invalid city"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", 'Response Content-Type should be application/json'

    json_response = response.json()
    value = json_response

    schema = load_schema("error_message")
    try:
        validate(instance=json_response, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e.message}")
    
    keys = ["cod", "message"]
    for key in keys:
        assert key in json_response, f"Response should contain key: {key}"
        assert isinstance(json_response[key], (int, str)), f"Response '{key}' should be an integer or string"
    
    assert json_response["cod"] == value["cod"], "Response 'cod' should match expected value"
    assert json_response["message"] == value["message"], "Response 'message' should match expected value"

    print("Test pertama berhasil dijalankan dengan sukses!")

