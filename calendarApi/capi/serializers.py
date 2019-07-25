from rest_framework import serializers
from .models import UserData,AssignementData

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = '__all__'

class assignedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignementData
        fields = '__all__'
