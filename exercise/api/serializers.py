from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Incident
from drf_extra_fields.geo_fields import PointField
from django.db import models

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups']
        # Campo password passa a ser visível nos métodos create ou update
        extra_kwargs = {
            'password': {'write_only': True}
        }
    # Override ao método create para poder ser definida a password do utilizador
    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
        ordering = ['-name']

class IncidentSerializer(serializers.HyperlinkedModelSerializer):
    longitude = serializers.CharField(required=False, write_only=True)  
    latitude = serializers.CharField(required=False, write_only=True) 
    
    class Meta:
        model = Incident
        fields = [
            'id', 
            'description',
            'author',
            'created',
            'updated',
            'status',
            'category',
            'location',
            'longitude',
            'latitude'
        ]
        
        # Author e Status são campos apenas de leitura.
        # Na criação de um objeto Incident, author=self.request.user
        # Status é colocado a Default, i.e., status='VALIDATED'
        extra_kwargs = {
            'author': {'read_only': True},
            #'status': {'read_only': True},
            'location': {'read_only': True},
        }
    
    

