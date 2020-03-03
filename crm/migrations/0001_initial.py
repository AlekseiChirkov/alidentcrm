# Generated by Django 3.0 on 2020-03-03 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('surname', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('day', models.DateField(verbose_name='День')),
                ('time', models.TimeField(unique=True, verbose_name='Время')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Сумма')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=16, verbose_name='День недели')),
            ],
            options={
                'verbose_name': 'Рабочий день',
                'verbose_name_plural': 'Рабочие дни',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.FloatField(verbose_name='Кодировка')),
                ('name', models.CharField(max_length=128, verbose_name='Услуга')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('surname', models.CharField(max_length=64, verbose_name='Фамилия')),
                ('patronymic', models.CharField(max_length=64, verbose_name='Отчество')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('username', models.CharField(max_length=64, unique=True, verbose_name='Телефон')),
                ('birthday', models.DateField(verbose_name='Дата рождения')),
                ('work_time', models.CharField(max_length=64, verbose_name='Режим работы')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Администратор')),
                ('is_staff', models.BooleanField(default=True, verbose_name='Персонал')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активность')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Суперпользователь')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=64, verbose_name='Статус')),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentage', models.IntegerField(verbose_name='Скидка в %')),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.Service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Акция',
                'verbose_name_plural': 'Акции',
            },
        ),
        migrations.AddField(
            model_name='service',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.ServiceCategory', verbose_name='Категория'),
        ),
        migrations.CreateModel(
            name='Income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Дата')),
                ('total_income', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Доход')),
                ('cheque', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Appointment', verbose_name='Чек')),
            ],
            options={
                'verbose_name': 'Доход',
                'verbose_name_plural': 'Доходы',
            },
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('expense_category', models.CharField(max_length=64, verbose_name='Категория расхода')),
                ('description', models.TextField(max_length=512, verbose_name='Примечания')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('date', models.DateField()),
                ('service', models.ManyToManyField(default=None, to='crm.Service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
            },
        ),
        migrations.CreateModel(
            name='Cheque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1, verbose_name='Количество')),
                ('price_per', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Цена за одну услугу')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Всего')),
                ('appointment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.Appointment', verbose_name='Запись')),
                ('service', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.Service', verbose_name='Услуга')),
                ('stock', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Stock', verbose_name='Акция')),
            ],
            options={
                'verbose_name': 'Чек',
                'verbose_name_plural': 'Чеки',
            },
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_income',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Income', verbose_name='Доход с записи'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.Staff'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='crm.Stage', verbose_name='Статус'),
        ),
    ]
