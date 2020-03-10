# Generated by Django 3.0 on 2020-03-10 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Имя')),
                ('surname', models.CharField(blank=True, max_length=64, null=True, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=64, null=True, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='Телефон')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='Email')),
                ('category', models.CharField(choices=[('Owner', 'Owner'), ('Doctor', 'Doctor'), ('Client', 'Client')], max_length=64, verbose_name='Категория пользователя')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Администратор')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Персонал')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперпользователь')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователя',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
