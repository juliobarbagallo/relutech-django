from django.urls import path, include
from rest_framework import routers
from .views import AssetViewSet

router = routers.DefaultRouter()
router.register(r'', AssetViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
