from rest_framework import serializers
from .models import Userdata,Assignementdata

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userdata
        fields = '__all__'

class assignedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignementdata
        fields = '__all__'