# Generated by Django 3.0 on 2020-04-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20200404_1811'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Ф.И.О.')),
                ('phone', models.CharField(max_length=16, verbose_name='Телефон')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
    ]
