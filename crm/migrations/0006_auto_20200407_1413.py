# Generated by Django 3.0 on 2020-04-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20200407_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cheque',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Общая сумма'),
        ),
        migrations.AlterField(
            model_name='cheque',
            name='client',
            field=models.CharField(max_length=128, verbose_name='Клиент'),
        ),
    ]
