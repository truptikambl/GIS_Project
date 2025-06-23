# maps/serializers.py

from rest_framework import serializers
from .models import State, District, Taluka, Village, Mahamarg

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ['id', 'name', 'state']


class TalukaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Taluka
        fields = ['id', 'name', 'district']


class VillageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'taluka']


class VillageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Village
        fields = ['id', 'name', 'population', 'pincode']


class MahamargSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahamarg
        fields = ['id', 'name']
