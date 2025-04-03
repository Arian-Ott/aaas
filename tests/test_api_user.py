from tests.api_client import AbstractAuthenticatedEndpointTest
from uuid import uuid4
from api.core.config import settings
import pytest
from api.schemas.user import CreateUser, UserUpdateSchema
import requests
import logging

class TestUsersAPI(AbstractAuthenticatedEndpointTest):

    @property
    def endpoint(self):
        return settings.API_PREFIX + "/users"

    def test_create_user(self):
        payload = CreateUser(
            id = uuid4(),
            username = f"testuser_{uuid4().hex}",
            password = "strongpassword123",
            email = f"test_{uuid4().hex}@example.com",
            is_active = True,
            
        )
        
        logging.info(payload)
        print(payload)
        response = self.auth_post("/register", data=payload.model_dump(mode="json"))
        print(response)
        assert response.status_code in (200, 201)
    def test_register_user_already_exists(self):
        payload = CreateUser(
            id = uuid4(),
            username = f"testuser_{uuid4().hex}",
            password = "strongpassword123",
            email= f"{uuid4().hex}@email.com",
            is_active = True,
        )
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload.model_dump(mode="json"))
        assert response.status_code == 200, f"First user creation failed, expected 200, got {response.status_code} with {response.json()}"
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload.model_dump(mode="json"))
        assert response.status_code == 400, f"Second user creation failed, expected 400, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "User already exists", f"Expected Username already exists, got {response.json()['detail']}"
    def test_get_users(self):
        response = self.auth_get("/all") #requests.get("http://127.0.0.1:8000" + self.endpoint + "/", headers=self._auth_headers())
        
        assert response.status_code == 200
        

    

    def test_unauthenticated_fails(self):
        res = requests.get("http://127.0.0.1:8000"+ self.endpoint + "/all")
        assert res.status_code == 401
    def test_duplicate_username(self):
        payload = CreateUser(
            id = uuid4(),
            username = f"testuser_{uuid4().hex}",
            password = "strongpassword123",
            email = f"test_{uuid4().hex}@example.com",
            is_active = True,
            
        )
        
      
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload.model_dump(mode="json"))
        logging.info(response.json())
        assert response.status_code == 200, "First user creation failed"
        payload.email = f"new_{uuid4().hex}@example.com"
        payload.id = uuid4()
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload.model_dump(mode="json"))
        assert response.status_code == 400, f"Second user creation failed, expected 400, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "User already exists", f"Expected Username already exists, got {response.json()['detail']}"
    
    def test_duplicate_email(self):
        payload = {
            "id": str(uuid4()),
            "username": "newuser",
            "email": f"new_{str(uuid4())}@example.com",
            "password": "secret123",
            "is_active": True
        }
      
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        logging.info(response.json())
        assert response.status_code == 200, f"First user creation failed, expected 200, got {response.status_code} with {response.json()}"
        payload["username"] = f"{uuid4()}"
        payload["id"] = str(uuid4())
        response = requests.post(f"http://127.0.0.1:8000{self.endpoint}/register", json=payload)
        assert response.status_code == 400, f"Second user creation failed, expected 400, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "Email already exists", f"Expected Email already exists, got {response.json()['detail']}"
    def test_me(self):
        response = self.auth_get("/me")
        assert response.status_code == 200
        assert response.json()["username"] == self._test_user_username
        assert response.json()["email"] == self._test_user_email
        assert response.json()["is_active"] == True
        assert response.json()["id"] == str(self._test_user_id)
    
    def test_me_not_authenticated(self):
    
        
        response = requests.get(f"http://127.0.0.1:8000{self.endpoint}/me", ) 
        assert response.status_code == 401, f"Expected 401, got {response.status_code} with {response.json()}"
        assert response.json()["detail"] == "Not authenticated", f"Expected Not authenticated, got {response.json()['detail']}" 
    
    def test_update_user(self):
        old_username = self._test_user_username
        old_email = self._test_user_email
        response = self.auth_post("/update", UserUpdateSchema( email=f"{uuid4().hex}@email.com", username=f"newusername_{uuid4().hex}").model_dump(mode="json")) 
        assert response.status_code == 200
        assert response.json()["username"] != old_username
        assert response.json()["email"] != old_email
        
    def test_delete_user(self):
        response = self.auth_delete("/me")
        assert response.status_code == 204
        assert response.content == b''


        
        
        