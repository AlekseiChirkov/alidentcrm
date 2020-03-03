from django.contrib import admin

from .models import *


class MyUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'name', 'surname', 'patronymic', 'birthday']
    list_display_links = ['username', 'name', 'surname', 'patronymic']

    class Meta:
        model = MyUser


admin.site.register(MyUser, MyUserAdmin)
