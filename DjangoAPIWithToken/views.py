from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse

from DjangoAPIWithToken.serializers import JWTTokenProviderSerializer


class MockView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return HttpResponse('mockview-get')

    def post(self, request):
        return HttpResponse('mockview-post')

class JWTTokenProviderView(APIView):
    http_method_names = ['post']
    serializer_class = JWTTokenProviderSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        print(serializer.validated_data)
        return Response(serializer.validated_data)
