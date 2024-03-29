from django.contrib.auth.models import User, Group
from api.models import Incident
from rest_framework import viewsets, status, permissions
from api.serializers import UserSerializer, GroupSerializer, IncidentSerializer
from django_filters import rest_framework as filters
from api.filters import UserFilter, IncidentFilter
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpRequest as Request
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create_auth(request):
    serializer = UserSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        user = serializer.save()
        group = Group.objects.get(name='Users') 
        group.user_set.add(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

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
        latitude = serializer.validated_data.pop('latitude')
        longitude = serializer.validated_data.pop('longitude')
        try:
            point = Point(float(longitude), float(latitude))
        except:
            raise ValidationError({'LocationError':'Longitude and Latitude values must be float'})

        serializer.save(author=self.request.user, location=point)

    @action(detail=False, methods=['GET'], name='Filter by location', )
    def filterByLocation(self, request):
        latitude = request.GET.get('latitude')
        longitude = request.GET.get('longitude')
        radius = request.GET.get('radius')

        try:
            float(radius)
            float(longitude)
            float(latitude)
            is_numeric = True
        except:
            is_numeric = False

        # Asserts necessários para que a extra action não rebente :)
        if not is_numeric:
            return Response({'ParametersError': 'Either \'radius\', \'longitude\' or \'latitude\' is None or it\'s not Numeric.'})

        # Ponto de partida, centro do raio de localização
        origin = Point(float(longitude), float(latitude))
        # Distância em quilómetros do raio de localização
        distance = Distance(km=float(radius))

        # Filtra e devolve todos os objectos do tipo Incident que estejam a uma distância menor que o raio de pesquisa
        queryset = Incident.objects.filter(location__distance_lte=(origin, distance))
	# Cria uma página com essa queryset
        page = self.paginate_queryset(queryset)

	# Se o resultado não for vazio, serializa o queryset e devolve esse resultado paginado
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
