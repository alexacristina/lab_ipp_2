from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from urllib.parse import parse_qs, urlparse

from oauth2_provider.models import get_application_model
from oauth2_provider.compat import get_user_model
from oauth2_provider.tests.test_utils import TestCaseUtils
from oauth2_provider.settings import oauth2_settings
import json

from rest_framework.test import APIRequestFactory, APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User

from authentication.views import UserViewSet

Application = get_application_model()
UserModel = get_user_model()


class BaseTest(TestCaseUtils, TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = UserModel.objects.create_user("test_user", "test@user.com", "123456")
        self.dev_user = UserModel.objects.create_user("dev_user", "dev@user.com", "123456")

        self.application = Application(
            name="Test Password Application",
            user=self.dev_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        self.client = APIClient()
        oauth2_settings._SCOPES = ['read', 'write']
        oauth2_settings._DEFAULT_SCOPES = ['read', 'write']

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()
        self.dev_user.delete()

class TestPasswordTokenView(BaseTest):
    def test_get_token(self):
        """
        Request an access token using Resource Owner Password Flow
        """
        token_request_data = {
            'grant_type': 'password',
            'username': 'test_user',
            'password': '123456',
        }
        auth_headers = self.get_basic_auth_header(self.application.client_id, self.application.client_secret)

        response = self.client.post(reverse('oauth2_provider:token'), data=token_request_data, **auth_headers)
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content['token_type'], "Bearer")
        self.assertEqual(content['scope'], "read write")
        self.assertEqual(content['expires_in'], oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)


class UserViewSetTestCase(APITestCase, TestCaseUtils):

    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.dev_user = User.objects.create_user("dev_user", "dev@user.com", "123456")
        self.post_view = UserViewSet.as_view({'post': 'create'})

        self.application = Application(
            name="Test Password Application",
            user=self.dev_user,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()

    def test_signup_new_user(self):
        new_user = {
            'grant_type': 'password',
            'username': 'test_user',
            'password': '123456',
        }
        auth_headers = self.get_basic_auth_header(self.application.client_id, self.application.client_secret)
        response = self.client.post(reverse('user-list'), data=new_user, **auth_headers)
        self.assertEqual(User.objects.count(), 2);

    def test_signup_bad_request(self):
        new_user = {
            'grant_type': 'password',
            'username': 'test_user_2'
        }
        auth_headers = self.get_basic_auth_header(self.application.client_id, self.application.client_secret)
        response = self.client.post(reverse('user-list'), data=new_user, **auth_headers)
        self.assertEqual(User.objects.count(), 1);
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        self.application.delete()
        self.dev_user.delete()
