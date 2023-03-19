from rest_framework import serializers
from .models import Asset

class AssetSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Asset
        fields = '__all__'