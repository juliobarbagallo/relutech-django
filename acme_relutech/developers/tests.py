import json

from developers.models import Developer
from developers.serializers import DeveloperSerializer
from developers.views import DeveloperViewSet
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate


class DeveloperModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.developer = Developer.objects.create(fullname="Mick Jagger", active=True)

    def test_developer_str_method(self):
        self.assertEqual(str(self.developer), "Mick Jagger")

    def test_developer_active_field(self):
        self.assertTrue(self.developer.active)


class DeveloperViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(
            username="testuser",
            password="testpass",
            email="testuser@acme.com",
        )
        self.developer = Developer.objects.create(fullname="Test Developer")

    def test_list_developers(self):
        request = self.factory.get("/api/developers/")
        force_authenticate(request, user=self.user)

        view = DeveloperViewSet.as_view({"get": "list"})
        response = view(request)

        serializer = DeveloperSerializer(Developer.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_developer(self):
        request = self.factory.get(
            reverse("developer-detail", kwargs={"pk": self.developer.pk})
        )
        force_authenticate(request, user=self.user)

        view = DeveloperViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.developer.pk)

        serializer = DeveloperSerializer(self.developer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_developer(self):
        data = {
            "fullname": "New Developer",
        }
        json_data = json.dumps(data)
        request = self.factory.post(
            "/api/developers/",
            data=json_data,
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)

        view = DeveloperViewSet.as_view({"post": "create"})
        response = view(request)

        serializer = DeveloperSerializer(
            Developer.objects.get(fullname="New Developer")
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_delete_developer(self):
        request = self.factory.delete(
            reverse("developer-detail", kwargs={"pk": self.developer.pk})
        )
        force_authenticate(request, user=self.user)

        view = DeveloperViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.developer.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Developer.objects.filter(id=self.developer.id).exists())

    def test_update_developer(self):
        data = {
            "fullname": "Updated Developer",
        }
        json_data = json.dumps(data)
        request = self.factory.put(
            reverse("developer-detail", kwargs={"pk": self.developer.pk}),
            data=json_data,
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)

        view = DeveloperViewSet.as_view({"put": "update"})
        response = view(request, pk=self.developer.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.developer.refresh_from_db()
        self.assertEqual(self.developer.fullname, "Updated Developer")
