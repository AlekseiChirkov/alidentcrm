from .models import *
from users.serializers import *


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'birthday', 'email']


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
    class Meta:
        model = Stock
        fields = '__all__'


class StockSerializerReadable(serializers.ModelSerializer):
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


class AppointmentSerializerReadable(serializers.ModelSerializer):
    doctor = StaffSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'time', 'phone', 'doctor', 'service', 'status']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSerializerReadable(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Expense
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Report
        fields = '__all__'


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'


class ChequeSerializerReadable(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = Cheque
        fields = '__all__'
