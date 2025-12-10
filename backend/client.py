import requests
from pydantic import BaseModel


class Client(BaseModel):
    model: str
    login: str
    password: str
    url: str
    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        response = requests.post(f"{self.url}/api/chat", json=payload, auth=(self.login, self.password))
        response_json = response.json()
        return response_json