from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *
from .forms import AppointmentForm
from .filters import CustomSearchFilter


def home(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.name = form.cleaned_data["name"]
            appointment.surname = form.cleaned_data["surname"]
            appointment.phone = form.cleaned_data["phone"]
            appointment.time = form.cleaned_data["time"]
            appointment.service = form.cleaned_data["service"]
            appointment.doctor = form.cleaned_data["doctor"]
            appointment.save()
            messages.success(request, "Successfully added appointment")
            return redirect('/')
    else:
        form = AppointmentForm()
    return render(request, 'crm/index.html', {'form': form})


class StaffViewSet(viewsets.ModelViewSet):
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


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

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
        except Client.DoesNotExist:
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


class StockViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def list(self, request, *args, **kwargs):
        stock = self.queryset.all()
        serializer = StockSerializerReadable(stock, many=True)
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


class ExpenseViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def list(self, request, *args, **kwargs):
        expense = self.queryset.all()
        serializer = ExpenseSerializerReadable(expense, many=True)
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


class ReportViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = (CustomSearchFilter, )
    search_fields = ['date']
    ordering_fields = '__all__'
    filterset_fields = ['date']

    def get(self):
        report = self.queryset.all()
        serializer = self.serializer_class(report, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            report = self.queryset.get(id=pk)
        except Report.DoesNotExist:
            raise Http404
        else:
            report.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class IncomeViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminUser,)
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get(self):
        user = MyUser.objects.values('category')
        print(user)
        income = self.queryset.all()
        serializer = self.serializer_class(income, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        pk = request.data.get('id', None)
        if pk is None:
            raise ParseError('role_id is required')

        try:
            income = self.queryset.get(id=pk)
        except Income.DoesNotExist:
            raise Http404
        else:
            income.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class ChequeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer

    def list(self, request, *args, **kwargs):
        cheque = self.queryset.all()
        serializer = ChequeSerializerReadable(cheque, many=True)
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
        except Expense.DoesNotExist:
            raise Http404
        else:
            cheque.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserAppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializerReadable
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['surname']

    # def list(self, request, *args, **kwargs):
    #     surname = request.query_params.get('surname', None)
    #     if surname:
    #         self.queryset = self.queryset.filter(surname=surname)
    #
    #     serializer = self.serializer_class(self.queryset, many=True)
    #
    #     return Response(serializer.data, status=200)


class DoctorAppointmentsViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializerReadable
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor']
