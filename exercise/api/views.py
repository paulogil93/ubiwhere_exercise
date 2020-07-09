from django.contrib.auth.models import User, Group
from api.models import Incident
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, IncidentSerializer
from django_filters import rest_framework as filters
from api.filters import UserFilter, IncidentFilter

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class IncidentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows incidents to be viewed or edited.
    """
    queryset = Incident.objects.all()
    serializer_class = IncidentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IncidentFilter

    # Override ao método perform_create para poder criar um objecto
    # do tipo Incident com o utilizador atual
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
