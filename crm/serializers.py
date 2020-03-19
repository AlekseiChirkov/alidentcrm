from rest_framework import serializers

from users.serializers import MyUserSerializer
from .models import *


class StaffSerializer(serializers.ModelSerializer):
    staff = MyUserSerializer()

    class Meta:
        model = Staff
        fields = ['staff']

    def create(self, validated_data):
        staff_data = validated_data.pop('staff')
        staff = MyUser.objects.create(**validated_data)
        MyUser.objects.create(staff=staff, **staff_data)


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    category = ServiceCategorySerializer()

    class Meta:
        model = Service
        fields = '__all__'

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = ServiceCategory.objects.create(**validated_data)
        Staff.objects.create(category=category, **category_data)


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
        fields = ['status']


class AppointmentSerializer(serializers.ModelSerializer):
    # doctor = StaffSerializer()
    # service = ServiceSerializer()
    # status = StageSerializer()

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'time', 'doctor', 'status', 'service']

    # def create(self, validated_data):
    #     doctor_data = validated_data.pop('doctor')
    #     doctor = Staff.objects.create(**validated_data)
    #     Staff.objects.create(staff=doctor, **doctor_data)
    #
    #     service_data = validated_data.pop('service')
    #     service = Service.objects.create(**validated_data)
    #     Service.objects.create(service=service, **service_data)
    #
    #     status_data = validated_data.pop('status')
    #     status = Stage.objects.create(**validated_data)
    #     Stage.objects.create(status=status, **status_data)
    #
    #     return doctor


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
