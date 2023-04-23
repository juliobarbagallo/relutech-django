from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from django.urls import reverse
from .models import Asset
from .serializers import AssetSerializer
from developers.models import Developer
from .views import AssetViewSet
import json

class AssetModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.developer = Developer.objects.create(fullname='Mick Jagger')
        cls.asset = Asset.objects.create(
            brand='Test Brand',
            model='Test Model',
            type='laptop',
            assigned_to=cls.developer,
        )

    def test_asset_str_method(self):
        self.assertEqual(str(self.asset), 'Test Brand Test Model')

    def test_asset_assigned_to_field(self):
        self.assertEqual(self.asset.assigned_to, self.developer)


class AssetViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
        )
        self.asset = Asset.objects.create(
            brand='testbrand',
            model='testmodel',
            type='laptop',
        )

    def test_list_assets(self):
        request = self.factory.get('/api/assets/')
        force_authenticate(request, user=self.user)

        view = AssetViewSet.as_view({'get': 'list'})
        response = view(request)

        serializer = AssetSerializer(Asset.objects.all(), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_asset(self):
        request = self.factory.get(f'/api/assets/{self.asset.id}/')
        force_authenticate(request, user=self.user)

        view = AssetViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.asset.id)

        serializer = AssetSerializer(self.asset)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_delete_asset(self):
        request = self.factory.delete(f'/api/assets/{self.asset.id}/')
        force_authenticate(request, user=self.user)

        view = AssetViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.asset.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Asset.objects.filter(id=self.asset.id).exists())

    def test_update_asset(self):
        data = {
            "brand": "newbrand",
            "model": "newmodel",
            "type": "laptop"
        }
        # request = self.factory.put(
        #     f'/api/assets/{self.asset.id}/',
        #     data={
        #         "brand": "newbrand",
        #         "model": "newmodel",
        #         "type": "laptop"
        #     },
        #     content_type='application/json',
        # )
        json_data = json.dumps(data)
        request = self.factory.put(
            f'/api/assets/{self.asset.id}/',
            data=json_data,
            content_type='application/json',
        )
        force_authenticate(request, user=self.user)

        view = AssetViewSet.as_view({'put': 'partial_update'})
        # print("REQUEST: ", request)
        response = view(request, pk=self.asset.id)
        # print("RRR: ", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.brand, 'newbrand')
        self.assertEqual(self.asset.model, 'newmodel')
        self.assertEqual(self.asset.type, 'laptop')