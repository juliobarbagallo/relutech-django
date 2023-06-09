from django.urls import include, path
from rest_framework import routers

from .views import DeveloperViewSet

router = routers.DefaultRouter()
router.register(r"", DeveloperViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
