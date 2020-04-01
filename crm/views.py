from django.http import Http404
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *


def home(request):
    return render(request, 'crm/index.html')


class StaffViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def get(self):
        user = self.queryset.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            user = self.queryset.get(id=pk)
        except Staff.DoesNotExist:
            raise Http404
        else:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

    def get(self):
        category = self.queryset.all()
        serializer = self.serializer_class(category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            category = self.queryset.get(id=pk)
        except ServiceCategory.DoesNotExist:
            raise Http404
        else:
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get(self):
        service = self.queryset.all()
        serializer = self.serializer_class(service, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def delete(self, request):
    #     pk = request.data.get('id', None)
    #     if pk is None:
    #         raise ParseError('role_id is required')
    #
    #     try:
    #         service = self.queryset.get(id=pk)
    #     except Service.DoesNotExist:
    #         raise Http404
    #     else:
    #         service.delete()
    #         return Response(status=status.HTTP_204_NO_CONTENT)


class StockViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get(self):
        stock = self.queryset.all()
        serializer = self.serializer_class(stock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            stock = self.queryset.get(id=pk)
        except Stock.DoesNotExist:
            raise Http404
        else:
            stock.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class DayViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Day.objects.all()
    serializer_class = DaySerializer

    def get(self):
        day = self.queryset.all()
        serializer = self.serializer_class(day, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            day = self.queryset.get(id=pk)
        except Day.DoesNotExist:
            raise Http404
        else:
            day.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def list(self, request, *args, **kwargs):
        appointment = self.queryset.all()
        serializer = AppointmentSerializerReadable(appointment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            appointment = self.queryset.get(id=pk)
        except Appointment.DoesNotExist:
            raise Http404
        else:
            appointment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ChequeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer

    def get(self):
        cheque = self.queryset.all()
        serializer = self.serializer_class(cheque, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            cheque = self.queryset.get(id=pk)
        except Cheque.DoesNotExist:
            raise Http404
        else:
            cheque.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get(self):
        expense = self.queryset.all()
        serializer = self.serializer_class(expense, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            expense = self.queryset.get(id=pk)
        except Expense.DoesNotExist:
            raise Http404
        else:
            expense.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)