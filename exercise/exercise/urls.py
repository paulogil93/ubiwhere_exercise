"""exercise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers
from api import views
from rest_framework_swagger.views import get_swagger_view

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'incidents', views.IncidentViewSet)
#router.register('register', views.create_auth, basename='register-user')

schema_view = get_swagger_view(title='Python & Django Ubiwhere API')

urlpatterns = [
    path('', include(router.urls)),
    path('docs/', schema_view),
    path('register/', views.create_auth),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
