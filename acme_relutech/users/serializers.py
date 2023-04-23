from rest_framework import serializers
from .models import User
from assets.models import Asset

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    assets = AssetSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
