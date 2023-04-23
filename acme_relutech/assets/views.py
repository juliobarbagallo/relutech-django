from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Asset
from .serializers import AssetSerializer
from rest_framework.response import Response



class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)