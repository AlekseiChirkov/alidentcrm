from rest_framework import serializers

from .models import *


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = '__all__'


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    category = ServiceCategorySerializer()

    class Meta:
        model = Service
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Appointment
        fields = '__all__'


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'