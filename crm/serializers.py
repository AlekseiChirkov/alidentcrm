from rest_framework import serializers

from users.serializers import MyUserSerializer
from .models import *


class StaffSerializer(serializers.ModelSerializer):
    staff = MyUserSerializer()

    class Meta:
        model = Staff
        fields = '__all__'


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer()

    class Meta:
        model = Service
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Stock
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['day']


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = StaffSerializer()
    service = ServiceSerializer()
    status = StageSerializer()

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'time', 'doctor', 'status', 'service']


class ChequeSerializer(serializers.ModelSerializer):
    appointment = AppointmentSerializer()
    service = ServiceSerializer()
    stock = StockSerializer()

    class Meta:
        model = Cheque
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Expense
        fields = '__all__'
