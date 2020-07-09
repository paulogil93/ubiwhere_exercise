from django.contrib.auth.models import User
from api.models import Incident
from django_filters import rest_framework as filters
from django.contrib.gis.db import models
from django import forms

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class IncidentFilter(filters.FilterSet):
    class Meta:
        model = Incident
        fields = ['author', 'category']