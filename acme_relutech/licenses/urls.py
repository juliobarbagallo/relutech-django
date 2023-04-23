from django.urls import path, include
from rest_framework import routers
from .views import LicenseViewSet

router = routers.DefaultRouter()
router.register(r'', LicenseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
