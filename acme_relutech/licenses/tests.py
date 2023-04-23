import json

from developers.models import Developer
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from licenses.models import License
from licenses.serializers import LicenseSerializer
from licenses.views import LicenseViewSet
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate


class LicenseModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.developer = Developer.objects.create(fullname="Mick Jagger")
        cls.license = License.objects.create(
            software="Test Software",
            assigned_to=cls.developer,
        )

    def test_license_str_method(self):
        self.assertEqual(str(self.license), "Test Software")

    def test_license_assigned_to_field(self):
        self.assertEqual(self.license.assigned_to, self.developer)


class LicenseViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(
            username="testuser",
            password="testpass",
            email="testuser@acme.com",
        )
        self.developer = Developer.objects.create(fullname="Test Developer")
        self.license = License.objects.create(
            software="Test Software",
            assigned_to=self.developer,
        )

    def test_list_licenses(self):
        request = self.factory.get("/api/licenses/")
        force_authenticate(request, user=self.user)

        view = LicenseViewSet.as_view({"get": "list"})
        response = view(request)

        serializer = LicenseSerializer(License.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_license(self):
        request = self.factory.get(
            reverse("license-detail", kwargs={"pk": self.license.pk})
        )
        force_authenticate(request, user=self.user)

        view = LicenseViewSet.as_view({"get": "retrieve"})
        response = view(request, pk=self.license.pk)

        serializer = LicenseSerializer(self.license)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_license(self):
        data = {
            "software": "New Software",
            "assigned_to": self.developer.pk,
        }
        json_data = json.dumps(data)
        request = self.factory.post(
            "/api/licenses/",
            data=json_data,
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)

        view = LicenseViewSet.as_view({"post": "create"})
        response = view(request)

        serializer = LicenseSerializer(License.objects.get(software="New Software"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_delete_license(self):
        request = self.factory.delete(
            reverse("license-detail", kwargs={"pk": self.license.pk})
        )
        force_authenticate(request, user=self.user)

        view = LicenseViewSet.as_view({"delete": "destroy"})
        response = view(request, pk=self.license.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(License.objects.filter(id=self.license.id).exists())

    def test_update_license(self):
        data = {
            "software": "Updated Software",
            "assigned_to": self.developer.pk,
        }
        json_data = json.dumps(data)
        request = self.factory.put(
            reverse("license-detail", kwargs={"pk": self.license.pk}),
            data=json_data,
            content_type="application/json",
        )
        force_authenticate(request, user=self.user)

        view = LicenseViewSet.as_view({"put": "update"})
        response = view(request, pk=self.license.pk)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.license.refresh_from_db()
        self.assertEqual(self.license.software, "Updated Software")
