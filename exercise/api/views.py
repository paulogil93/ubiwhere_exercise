from django.contrib.auth.models import User, Group
from api.models import Incident
from rest_framework import viewsets
from api.serializers import UserSerializer, GroupSerializer, IncidentSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

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

    # Override ao método perform_create para poder criar um objecto
    # do tipo Incident com o utilizador atual
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
