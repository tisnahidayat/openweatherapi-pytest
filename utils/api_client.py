import requests as req
from dotenv import load_dotenv
import os

load_dotenv()

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        self.api_key = os.getenv("API_KEY")
        if not self.base_url:
            raise ValueError("BASE_URL must be set in the .env file")
        self.headers = {
            "Content-Type": "application/json"
        }

    def get(self, endpoint, params=None):
        url = f"{self.base_url}/{endpoint}"

        if self.api_key:
            params = {"appid": self.api_key, **(params or {})}
        else:
            params = params if params is not None else {}

        response = req.get(url, headers=self.headers, params=params)
        return response
