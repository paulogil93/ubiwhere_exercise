from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models import Incident

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
    class Meta:
        model = Incident
        fields = [
            'id', 
            'description',
            'location',
            'author',
            'created',
            'updated',
            'status',
            'category'
        ]
