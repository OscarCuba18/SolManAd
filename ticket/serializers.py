from rest_framework import serializers
from .models import MaintenanceRequest, Assignament

class MaintenanceRequest_Serializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'

class Assignament_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Assignament
        fields = '__all__'