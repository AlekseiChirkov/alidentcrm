from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def get(self):
        user = self.queryset.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.method == 'POST':
            serializer = self.serializer_class(data=request.data)
            data = {}
            if serializer.is_valid():
                account = serializer.save()
                data['response'] = "Successfully registered a new user"
                data['email'] = account.email
                data['username'] = account.username
            else:
                data = serializer.errors
            return Response(data)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            user = self.queryset.get(id=pk)
        except MyUser.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
