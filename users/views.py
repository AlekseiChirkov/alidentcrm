from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ParseError

from .serializers import *
from .models import *


def email_to_clients():
    queryset = MyUser.objects.all().filter(category='Client')

    subject = 'Пора на обследование!'
    message = 'Как давно вы проверяли свои зубы? Прора их проверить! Ведь от здоровья Вашей ротовой полости зависит ' \
              'здоровье почти всего вашего организма! '
    email_from = settings.EMAIL_HOST_USER
    for user in queryset:
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)

    return message('OK')


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
            raise ParseError('id is required')

        try:
            user = self.queryset.get(id=pk)
        except MyUser.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
