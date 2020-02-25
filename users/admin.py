from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

    class Meta:
        model = Category


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'patronymic', 'birthday', 'email', 'phone', 'category']
    list_display_links = ['name', 'surname', 'patronymic', 'email', 'phone']

    class Meta:
        model = MyUser


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Category, CategoryAdmin)
