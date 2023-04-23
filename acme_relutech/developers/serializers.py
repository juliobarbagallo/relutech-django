from assets.models import Asset
from licenses.models import License
from rest_framework import serializers

from .models import Developer


class AssetSerializerFD(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = "__all__"


class LicenseSerializerFD(serializers.ModelSerializer):
    class Meta:
        model = License
        fields = "__all__"


class DeveloperSerializer(serializers.ModelSerializer):
    assets = AssetSerializerFD(many=True, read_only=True)
    licenses = LicenseSerializerFD(many=True, read_only=True)

    class Meta:
        model = Developer
        fields = "__all__"
        ref_name = "DeveloperSerializer"
