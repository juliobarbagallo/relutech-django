from django.urls import include, path
from rest_framework import routers

from .views import LicenseViewSet

router = routers.DefaultRouter()
router.register(r"", LicenseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
