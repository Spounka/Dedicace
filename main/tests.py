from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from model_bakery import baker
from . import views, serializers, models


# Create your tests here.
class ClientTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = baker.make(models.Client, _quantity=5)
        print(self.user[1].wilaya)

    def test_return_current_client(self):
        request = self.factory.post("client/")
        force_authenticate(request, user=self.user[1].user)
        views.ClientCurrent().as_view()(request)
        self.assertTrue(request.user.is_authenticated)
        self.assertEqual(request.user.client, self.user[1])

    def test_create_client_201(self):
        serializer = serializers.ClientSerializer(self.user)
        request = self.factory.post('client/create/', data=serializer.data, format='json')
        response = views.ClientCreate().as_view()(request)
        print(response.content)
        self.assertTrue(response.status_code, 201)
