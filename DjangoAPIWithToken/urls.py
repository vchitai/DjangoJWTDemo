"""DjangoAPIWithToken URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.models import User
import rest_framework_jwt.authentication as a

from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework_jwt import views
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class MockView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return HttpResponse('mockview-get')

    def post(self, request):
        return HttpResponse('mockview-post')


urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api-token-auth/', views.obtain_jwt_token),
    url(r'^auth-token-refresh/$', views.refresh_jwt_token),
    url(r'^auth-token-verify/$', views.verify_jwt_token),

    url(r'^jwt/$', MockView.as_view(
        authentication_classes=[JSONWebTokenAuthentication])),
]
# user = User.objects.create_user('tai', 'abc@email.com', '123123')
# user.save()
