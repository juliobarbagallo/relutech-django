from rest_framework import serializers
from .models import Developer
from assets.models import Asset
from licenses.models import License


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class LicenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = '__all__'


class DeveloperSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)
    licenses = LicenseSerializer(many=True, read_only=True)

    class Meta:
        model = Developer
        fields = '__all__'
