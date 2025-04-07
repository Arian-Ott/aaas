from tests.api_client import AbstractAuthenticatedEndpointTest
from api.core.deps import settings
import os
import pytest
import logging
class SecurityTest(AbstractAuthenticatedEndpointTest):
    """
    Test the security of the API.
    """
    @property
    def endpoint(self):
        
        return settings.API_PREFIX +  "/sagw"

    def test_get_public_key(self):
        """
        Test the public key endpoint.
        """
        print(self.endpoint)
        response = self.client.get(f"{self.endpoint}/public_key")
        assert response.status_code == 200
        assert "public_key" in response.json()
        assert "alg" in response.json()
        assert "use" in response.json()
        assert response.json()["alg"] == "ES512"
        
        lv_public_key = open("api/core/certs/ec-public.pem", "r").read()
        assert lv_public_key in response.json()["public_key"]
        assert response.json()["use"] == "sig"
        logging.info(response.json())
        print(response.json())
    def test_get_public_key_not_found(self):
        """
        Test the public key endpoint with a non-existent key.
        """
        
        resp = self.client.get(f"{self.endpoint}/public_key")
        print(resp)
        
    