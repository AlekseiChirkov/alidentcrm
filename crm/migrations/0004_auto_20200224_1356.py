# Generated by Django 3.0 on 2020-02-24 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20200224_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='income',
            name='cheque',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Appointment', verbose_name='Чек'),
        ),
    ]
