
import pytest, json
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.mark.positive
def test_setup(api_client):

    response = api_client.get("data/2.5/weather", params={"lat": 51.5074, "lon": -0.1278})

    assert response is not None, f"Response should not be None"
    assert isinstance(response, dict), "Response should be a dictionary"

    value = response
    
    schema = load_schema("current_weather_data")
    try:
        validate(instance=response, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e.message}")
    
    assert response["cod"] == 200
    keys = ["coord", "weather", "main", "wind", "name"]
    for key in keys:
        assert key in response, f"Response should contain key: {key}"
        # assert ininstance(response[key], (dict, list, int, str)), f"Response '{key}' should be a dictionary, list, int, or string"

    assert isinstance(response["coord"], dict), "Response 'coord' should be a dictionary"
    assert isinstance(response["weather"], list), "Response 'weather' should be a list"
    assert isinstance(response["main"], dict), "Response 'main' should be a dictionary"
    assert isinstance(response["wind"], dict), "Response 'wind' should be a dictionary"
    assert isinstance(response["name"], str), "Response 'name' should be a string"
    
    assert response["coord"]["lat"] == value["coord"]["lat"]
    assert response["coord"]["lon"] == value["coord"]["lon"]
    assert response["weather"][0]["main"] == value["weather"][0]["main"]
    assert response["weather"][0]["description"] == value["weather"][0]["description"]
    assert response["main"]["temp"] == value["main"]["temp"]
    assert response["wind"]["speed"] == value["wind"]["speed"]
    assert response["wind"]["deg"] == value["wind"]["deg"]
    assert response["name"] == value["name"]

    assert isinstance(response["coord"]["lat"], float), "Response 'coord.lat' should be a string"
    assert isinstance(response["coord"]["lon"], float), "Response 'coord.lon' should be a string"
    assert isinstance(response["weather"][0]["main"], str), "Response 'weather.main' should be a string"
    assert isinstance(response["weather"][0]["description"], str), "Response 'weather.description' should be a string"
    assert isinstance(response["main"]["temp"], float), "Response 'main.temp' should be a float"
    assert isinstance(response["wind"]["speed"], float), "Response 'wind.speed' should be a float"
    assert isinstance(response["wind"]["deg"], int), "Response 'wind.deg' should be an integer"
    assert isinstance(response["name"], str), "Response 'name' should be a string"

    print("Test pertama berhasil dijalankan dengan sukses!")

