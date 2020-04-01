from django.contrib import admin

from .models import *


class ChequeInline(admin.TabularInline):
    model = Cheque
    fields = ('service', 'count', 'price_per', 'total_price', 'stock')
    extra = 0


class AppointmentInline(admin.TabularInline):
    model = Appointment
    fields = ('name', 'surname', 'day', 'time', 'total_price')
    extra = 0


class StaffAdmin(admin.ModelAdmin):
    list_display = ['name']

    class Meta:
        model = Staff


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
    inlines = [ChequeInline]
    exclude = ['appointment_income']
    readonly_fields = ('total_price',)

    class Meta:
        model = Appointment


class IncomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Income._meta.fields]
    inlines = [AppointmentInline]

    class Meta:
        model = Income


class ChequeAdmin(admin.ModelAdmin):
    list_display = ['appointment', 'service', 'count', 'price_per', 'total_price', 'stock']

    class Meta:
        model = Cheque


class ExpenseAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Expense._meta.fields]

    class Meta:
        model = Expense


admin.site.register(Staff, StaffAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Day, DayAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)
