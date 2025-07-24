
import pytest, json
from utils.api_client import APIClient
from utils.schema_loader import load_schema
from jsonschema import validate, ValidationError

@pytest.fixture(scope="session")
def api_client():
    return APIClient()

@pytest.mark.positive
def test_forecast_city(api_client):

    response = api_client.get("data/2.5/forecast", params={"q": "London"})

    json_response = response.json()
    value = json_response

    assert response.status_code == 200, "Response status code should be 200"
    assert response.headers["Content-Type"] == "application/json; charset=utf-8", "Response Content-Type should be application/json"
    
    schema = load_schema("forecast_weather")
    try:
        validate(instance=json_response, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e.message}")
    
    keys = ["list", "city"]
    for key in keys:
        assert key in json_response, f"Response should contain key: {key}"
        # assert ininstance(response[key], (dict, list, int, str)), f"Response '{key}' should be a dictionary, list, int, or string"

    assert isinstance(json_response["city"], dict), "Response 'coord' should be a dictionary"
    assert isinstance(json_response["city"]["name"], str), "Response 'city.name' should be a string"
    assert isinstance(json_response["list"], list), "Response 'list' should be a list"
    assert isinstance(json_response["list"][0]["main"], dict), "Response 'list.main' should be a dictionary"
    assert isinstance(json_response["list"][0]["weather"], list), "Response 'list.weather' should be a list"
    assert isinstance(json_response["list"][0]["wind"], dict), "Response 'list.wind' should be a list"
    
    assert json_response["list"][0]["main"]["temp"] == value["list"][0]["main"]["temp"]
    assert json_response["list"][0]["weather"][0]["main"] == value["list"][0]["weather"][0]["main"]
    assert json_response["list"][0]["weather"][0]["description"] == value["list"][0]["weather"][0]["description"]
    assert json_response["list"][0]["wind"]["speed"] == value["list"][0]["wind"]["speed"]
    assert json_response["city"]["name"] == value["city"]["name"]

    assert isinstance(json_response["list"][0]["main"]["temp"], (float, int)), "Response 'list.main.temp' should be a float or integer"
    assert isinstance(json_response["list"][0]["weather"][0]["main"], str), "Response 'list.weather.main' should be a string"
    assert isinstance(json_response["list"][0]["weather"][0]["description"], str), "Response 'weather.description' should be a string"
    assert isinstance(json_response["list"][0]["wind"]["speed"], (float, int)), "Response 'list.wind.speed' should be a float or integer"
    assert isinstance(json_response["city"]["name"], str), "Response 'city.name' should be a string"

