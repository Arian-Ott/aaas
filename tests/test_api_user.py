from tests.api_client import AbstractAuthenticatedEndpointTest
from uuid import uuid4
from api.core.config import settings
import pytest
import requests
import logging
class TestUsersAPI(AbstractAuthenticatedEndpointTest):

    @property
    def endpoint(self):
        return settings.API_PREFIX + "/users"

    def test_create_user(self):
        payload = {
            "id": str(uuid4()),
            "username": "newuser",
            "email": f"new_{uuid4().hex[:6]}@example.com",
            "password": "secret123",
            "is_active": True
        }
        response = self.auth_post("/register", data=payload)
        assert response.status_code in (200, 201)

    def test_get_users(self):
        response = self.auth_get("/all") #requests.get("http://127.0.0.1:8000" + self.endpoint + "/", headers=self._auth_headers())
        
        assert response.status_code == 200
        
        assert isinstance(response.json(), list)
    

    def test_unauthenticated_fails(self):
        res = requests.get("http://127.0.0.1:8000"+ self.endpoint + "/all")
        assert res.status_code == 401
    def test_duplicate_username(self):
        payload = {
            "id": str(uuid4()),
            "username": "newuser",
            "email": f"new_{uuid4().hex[:6]}@example.com",
            "password": "secret123",
            "is_active": True
        }
      
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        logging.info(response.json())
        assert response.status_code == 200, "First user creation failed"
        payload["email"] = f"new_{uuid4().hex[:6]}@example.com"
        payload["id"] = str(uuid4())
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        assert response.status_code == 400, f"Second user creation failed, expected 400, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "User already exists", f"Expected Username already exists, got {response.json()['detail']}"
    
    def test_duplicate_email(self):
        payload = {
            "id": str(uuid4()),
            "username": "newuser",
            "email": f"new_{uuid4().hex[:6]}@example.com",
            "password": "secret123",
            "is_active": True
        }
      
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        logging.info(response.json())
        assert response.status_code == 200, f"First user creation failed, expected 200, got {response.status_code} with {response.json()}"
        payload["username"] = f"new_{uuid4().hex[:6]}"
        payload["id"] = str(uuid4())
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        assert response.status_code == 400, f"Second user creation failed, expected 400, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "Email already exists", f"Expected Email already exists, got {response.json()['detail']}"
    
        
            