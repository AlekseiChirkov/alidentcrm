from django.contrib import admin
from solo.admin import SingletonModelAdmin

from .models import *


class StaffAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        model = Staff


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        model = Client


class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ServiceCategory._meta.fields]

    class Meta:
        model = ServiceCategory


class ServiceAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Service._meta.fields]

    class Meta:
        model = Service


class StockAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Stock._meta.fields]

    class Meta:
        model = Stock


class DayAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Day._meta.fields]

    class Meta:
        model = Day


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'time', 'doctor', 'total_price', 'status', 'service']
    exclude = ['appointment_income']
    readonly_fields = ('total_price',)

    class Meta:
        model = Appointment


class ExpenseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Expense._meta.fields]

    class Meta:
        model = Expense


class ReportAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Report._meta.fields]

    class Meta:
        model = Report


class IncomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Income._meta.fields]

    class Meta:
        model = Income


class ChequeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cheque._meta.fields]

    class Meta:
        model = Cheque


admin.site.register(Staff, StaffAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Income, SingletonModelAdmin)
admin.site.register(Cheque, ChequeAdmin)
