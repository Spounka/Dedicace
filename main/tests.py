from django.test import TestCase
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIRequestFactory, force_authenticate, APITestCase, APIClient

from . import views
from .models import User, Client


def create_client() -> Client:
    phone_number = '+213669344926'
    username = 'hohi'
    password = 'rootuser'
    email = 'something@something.com'
    user = User.objects.create_user(phone_number=phone_number, username=username, password=password,
                                    email=email)
    client = Client.objects.create(user=user, wilaya='34')
    return client


# Create your tests here.
class TestCurrentModel(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        user = User.objects.create_user(phone_number='+213333333333', username='hoho', password='rootuser')
        self.client = Client.objects.create(user=user, wilaya='34')

    def test_client_authenticated_passes(self):
        # assign
        request = self.factory.get(reverse_lazy('client-current'))
        force_authenticate(request, self.client.user)
        view = views.ClientCurrent.as_view()

        # act
        response: Response = view(request)

        # assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('user').get('phone_number'), self.client.user.phone_number)

    def test_client_unauthenticated_fails(self):
        # assign
        request = self.factory.get(reverse_lazy('client-current'))

        # act
        view = views.ClientCurrent().as_view()
        response = view(request)

        # assert
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class TestCreateClient(APITestCase):
    def setUp(self) -> None:
        self.data = {
            'user':   {
                'phone_number': '0669344935',
                'username':     'hihihi',
                'password':     'rootuser',
                'first_name':   'suss',
                'last_name':    'duss'
            },
            'wilaya': 34

        }
        self.response: Response = self.client.post(reverse_lazy('client-create'), data=self.data, format='json')

    def test_send_correct_data_passes(self):
        # assign

        # act

        # assert
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertGreaterEqual(Client.objects.count(), 1)
        self.assertEqual(User.objects.all().first().phone_number,
                         User.normalize_username(self.data.get('user').get('phone_number')))

    def test_created_client_is_authenticated(self):
        # assign
        # act

        # assert
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertIn('_auth_user_id', self.client.session)

    def test_created_client_token_is_valid(self):
        # assign
        token_response = self.response
        # act
        _token: str = token_response.data.get('token')

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Token {_token}')
        user_response: Response = client.get(reverse_lazy('client-current'))

        # assert
        self.assertIsNotNone(_token)
        self.assertEqual(user_response.data.get('user').get('phone_number'),
                         User.normalize_username(self.data.get('user').get('phone_number')))

    def test_send_duplicate_phone_number_fails(self):
        # assign
        data = {
            'user': {
                'phone_number': self.data.get('user').get('phone_number'),
                'username':     'something_new',
                'email':        39
            }
        }
        # act
        response = self.client.post(reverse_lazy('client-create'), data=data, format='json')
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_send_no_nested_data_fails(self):
        # assign
        data = {
            'useraname':    'someone_haka',
            'phone_number': '0669344980',
            'email':        "someone@something.com",
            'password':     'rootuser'
        }

        # act
        response = self.client.post(reverse_lazy('client-create'), data=data, format='json')

        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_data_fails(self):
        # act
        response = self.client.post(reverse_lazy('client-create'), data={}, format='json')
        # assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
