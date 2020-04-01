from .models import *
from users.serializers import *


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'name']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        exclude = ('id', )


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['day']


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'time', 'doctor', 'service', 'status']

    # def create(self, validated_data):
    #     service_data = validated_data.pop('service')
    #     service = Service.objects.create(**service_data)
    #     appointment = Appointment.objects.create(service=service, **validated_data)
    #
    #     return appointment


class AppointmentSerializerReadable(serializers.ModelSerializer):
    doctor = StaffSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'time', 'doctor', 'service', 'status']


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
