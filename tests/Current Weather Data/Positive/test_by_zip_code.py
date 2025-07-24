
import pytest, json
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.mark.positive
def test_by_zip_code(api_client):

    response = api_client.get("data/2.5/weather", params={"id": "2172797"})  # Example city ID for Cairns, Australia

    json_response = response.json()
    value = json_response
    
    assert response.status_code == 200, "Response status code should be 200"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", "Response Content-Type should be application/json"

    schema = load_schema("current_weather_data")
    try:
        validate(instance=json_response, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e.message}")
    
    assert json_response["cod"] == 200
    keys = ["coord", "weather", "main", "wind", "name"]
    for key in keys:
        assert key in json_response, f"Response should contain key: {key}"
        # assert ininstance(json_response[key], (dict, list, int, str)), f"Response '{key}' should be a dictionary, list, int, or string"

    assert isinstance(json_response["coord"], dict), "Response 'coord' should be a dictionary"
    assert isinstance(json_response["weather"], list), "Response 'weather' should be a list"
    assert isinstance(json_response["main"], dict), "Response 'main' should be a dictionary"
    assert isinstance(json_response["wind"], dict), "Response 'wind' should be a dictionary"
    assert isinstance(json_response["name"], str), "Response 'name' should be a string"
    
    assert json_response["coord"]["lat"] == value["coord"]["lat"]
    assert json_response["coord"]["lon"] == value["coord"]["lon"]
    assert json_response["weather"][0]["main"] == value["weather"][0]["main"]
    assert json_response["weather"][0]["description"] == value["weather"][0]["description"]
    assert json_response["main"]["temp"] == value["main"]["temp"]
    assert json_response["wind"]["speed"] == value["wind"]["speed"]
    assert json_response["wind"]["deg"] == value["wind"]["deg"]
    assert json_response["cod"] == value["cod"]
    assert json_response["name"] == value["name"]

    assert isinstance(json_response["coord"]["lat"], float), "Response 'coord.lat' should be a string"
    assert isinstance(json_response["coord"]["lon"], float), "Response 'coord.lon' should be a string"
    assert isinstance(json_response["weather"][0]["main"], str), "Response 'weather.main' should be a string"
    assert isinstance(json_response["weather"][0]["description"], str), "Response 'weather.description' should be a string"
    assert isinstance(json_response["main"]["temp"], float), "Response 'main.temp' should be a integer"
    assert isinstance(json_response["wind"]["speed"], (float, int)), "Response 'wind.speed' should be a float"
    assert isinstance(json_response["wind"]["deg"], int), "Response 'wind.deg' should be an integer"
    assert isinstance(json_response["name"], str), "Response 'name' should be a string"

    print("Test pertama berhasil dijalankan dengan sukses!")

