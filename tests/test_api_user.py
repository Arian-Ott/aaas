from tests.api_client import AbstractAuthenticatedEndpointTest
from uuid import uuid4
from api.core.config import settings

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
        response = self.auth_get("/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    

    def test_unauthenticated_fails(self):
        res = self.client.get(f"{self.endpoint}/")
        assert res.status_code == 401