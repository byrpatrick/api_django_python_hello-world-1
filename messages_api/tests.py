from time import time
from unittest.mock import patch

from django.test import SimpleTestCase
from rest_framework.reverse import reverse
from rest_framework_simplejwt.backends import TokenBackend

from messages_api.views import (
    PublicMessageApiView, AuthMessageApiView, AdminMessageApiView
)

VALID_TOKEN_PAYLOAD = {
    "iss": "https://my-domain.us.auth0.com/",
    "sub": "user@clients",
    "aud": "https://api.example.com",
    "iat": time(),
    "exp": time() + 3600,
    "azp": "mK3brgMY0GIMox40xKWcUZBbv2Xs0YdG",
    "scope": "read:messages",
    "gty": "client-credentials",
    "permissions": [],
}

ADMIN_TOKEN_PAYLOAD = {
    **VALID_TOKEN_PAYLOAD,
    "permissions": ["read:admin-messages"],
}


class PublicMessageApiViewTest(SimpleTestCase):

    def test_public_api_view_returns_ok(self):
        response = self.client.get(reverse('public-message'))

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.json(), {'message': PublicMessageApiView.message})


class AuthMessageApiViewTest(SimpleTestCase):

    def test_protected_api_view_without_token_returns_unauthorized(self):
        response = self.client.get(reverse('protected-message'))

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': "Authentication credentials were not provided."}
        )

    def test_protected_api_view_with_invalid_token_returns_unauthorized(self):
        response = self.client.get(
            reverse('protected-message'), HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': "Given token not valid for any token type"}
        )

    @patch.object(TokenBackend, 'decode')
    def test_protected_api_view_with_valid_token_returns_ok(self, mock_decode):
        mock_decode.return_value = VALID_TOKEN_PAYLOAD

        response = self.client.get(
            reverse('protected-message'), HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {'message': "The API successfully validated your access token."},
        )


class AdminMessageApiViewTest(SimpleTestCase):

    def test_admin_api_view_without_token_returns_unauthorized(self):
        response = self.client.get(reverse('admin-message'))

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': "Authentication credentials were not provided."}
        )

    def test_admin_api_view_with_invalid_token_returns_unauthorized(self):
        response = self.client.get(
            reverse('admin-message'), HTTP_AUTHORIZATION="Bearer invalid-token"
        )

        self.assertEqual(response.status_code, 401)
        self.assertDictEqual(
            response.json(), {'message': "Given token not valid for any token type"}
        )

    @patch.object(TokenBackend, 'decode')
    def test_admin_api_view_without_admin_token_returns_forbidden(self, mock_decode):
        mock_decode.return_value = VALID_TOKEN_PAYLOAD

        response = self.client.get(
            reverse('admin-message'), HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 403)
        self.assertDictEqual(
            response.json(),
            {'message': "You do not have permission to perform this action."},
        )

    @patch.object(TokenBackend, 'decode')
    def test_admin_api_view_with_admin_token_returns_ok(self, mock_decode):
        mock_decode.return_value = ADMIN_TOKEN_PAYLOAD

        response = self.client.get(
            reverse('admin-message'), HTTP_AUTHORIZATION="Bearer valid-token"
        )

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {'message': "The API successfully recognized you as an admin."},
        )
