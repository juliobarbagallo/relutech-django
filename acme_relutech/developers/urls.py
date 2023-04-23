from django.urls import path, include
from rest_framework import routers
from .views import DeveloperViewSet

router = routers.DefaultRouter()
router.register(r'', DeveloperViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
