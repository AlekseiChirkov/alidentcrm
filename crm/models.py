from datetime import datetime

from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from solo.models import SingletonModel
from decimal import Decimal

from users.models import MyUser


class Staff(models.Model):
    name = models.CharField(verbose_name='Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name='Телефон', max_length=16)
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(blank=True, null=True)
    experience = models.IntegerField(verbose_name='Опыт работы', blank=True, null=True, default=0)
    specialization = models.CharField(verbose_name='Специализация', max_length=64, blank=True, null=True, default=None)
    date = models.DateField(verbose_name='Дата регистрации', auto_now=True)

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=MyUser)
def make_doctor(sender, instance, created, **kwargs):
    if instance.category == 'Персонал':
        if created:
            staff = Staff.objects.create(
                name=instance.name + ' ' + instance.surname + ' ' + instance.patronymic,
                phone=instance.username,
                birthday=instance.birthday,
                email=instance.email
            )
            staff.save()


class Client(models.Model):
    name = models.CharField(verbose_name='Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name='Телефон', max_length=16)
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(blank=True, null=True)
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=MyUser)
def make_client(sender, instance, created, **kwargs):
    if instance.category == 'Клиент':
        if created:
            client = Client.objects.create(
                name=instance.name + ' ' + instance.surname + ' ' + instance.patronymic,
                phone=instance.username,
                birthday=instance.birthday,
                email=instance.email
            )
            client.save()


class ServiceCategory(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Service(models.Model):
    code = models.FloatField(verbose_name='Кодировка', unique=True)
    name = models.CharField(verbose_name='Услуга', max_length=128)
    category = models.ForeignKey(ServiceCategory, verbose_name='Категория', on_delete=models.CASCADE, default=None)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return f"{self.name}, {self.price} сом"


class Stock(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=64)
    description = models.CharField(verbose_name='Описание', max_length=256)
    percentage = models.IntegerField(verbose_name='Скидка в %')
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return '%s' % self.percentage


class Day(models.Model):
    day = models.CharField(verbose_name='День недели', max_length=16)

    class Meta:
        verbose_name = "Рабочий день"
        verbose_name_plural = "Рабочие дни"

    def __str__(self):
        return self.day


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Активен', 'Активен'),
        ('Завершен', 'Завершен'),
        ('Приостановлен', 'Приостановлен'),
        ('Отменен', 'Отменен')
    )
    name = models.CharField(verbose_name='Имя', max_length=64)
    surname = models.CharField(verbose_name='Фамилия', max_length=64)
    phone = models.CharField(verbose_name='Телефон клиента', max_length=64)
    time = models.DateTimeField(verbose_name='Время', null=True)
    doctor = models.ForeignKey(Staff, verbose_name='Врач', on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2, default=0)
    status = models.CharField(verbose_name='Статус', max_length=64, choices=STATUS_CHOICES, default='Активен')
    appointment_income = models.ForeignKey('Income', verbose_name='Доход с записи', on_delete=models.CASCADE,
                                           default=None, null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE, default=None)
    stock = models.ForeignKey(Stock, verbose_name='Акция', on_delete=models.CASCADE, default=None, blank=True, null=True)
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return '%s %s %s' % (
            self.name, self.surname, self.time
        )

    def save(self, *args, **kwargs):
        price = self.service.price
        if self.stock:
            stock = self.stock.percentage * 0.01
            stock_price = Decimal(price) - Decimal(price) * Decimal(stock)
            self.total_price = Decimal(stock_price)
        else:
            self.total_price = price
        super(Appointment, self).save(*args, **kwargs)


class Expense(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    category = models.CharField(verbose_name='Категория расхода', max_length=64)
    description = models.CharField(verbose_name='Описание', max_length=128)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость (сом)', max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def __str__(self):
        return '%s %s %s %s %s %s' % (
            self.name, self.category, self.description, self.service, self.price, self.date
        )


class Report(models.Model):
    service = models.ForeignKey(Service, verbose_name='Название услуги', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Записей за день')
    price = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name='Дата отчета', auto_now_add=True)

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"

    def __str__(self):
        return '%s %s %s %s' % (self.service, self.count, self.price, self.date)


@receiver(post_save, sender=Appointment)
def make_report(sender, instance, created, **kwargs):
    qs = Appointment.objects.values('service', 'service__report__date'). \
        annotate(count=Count('name'), sum=Sum('service__price'))
    for service in qs:
        serv = Service.objects.get(id=service['service'])
        try:
            report = Report.objects.get(date=service['service__report__date'], service=serv)
        except Report.DoesNotExist:
            Report.objects.create(service=serv,
                                  count=service['count'],
                                  price=service['sum'], )
            continue
        report.count = service['count']
        report.price = service['sum']
        report.save()


class Cheque(models.Model):
    client = models.CharField(verbose_name='Клиент', max_length=128)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0)
    date = models.DateField(verbose_name='Дата чека', auto_now_add=True)
    stock = models.ForeignKey(Stock, verbose_name='Скидка', on_delete=models.CASCADE, blank=True, null=True, default=None)
    amount = models.DecimalField(verbose_name='Общая сумма', max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'Чек: {self.client}'

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def save(self, *args, **kwargs):
        if self.stock:
            stock_value = self.stock.percentage * 0.01
            stock = float(self.price) * stock_value
            amount = float(self.price) - stock
            self.amount = amount
            super(Cheque, self).save(*args, **kwargs)


@receiver(post_save, sender=Appointment)
def create_cheque(sender, instance, created, **kwargs):
    if instance.status == 'Завершен':
        cheque = Cheque.objects.create(
            client=instance.name + ' ' + instance.surname,
            service=instance.service,
            price=instance.service.price,
            stock=instance.stock
        )
        cheque.save()


class Income(SingletonModel):
    finished = models.IntegerField(verbose_name='Завершенных записей', default=0)
    canceled = models.IntegerField(verbose_name='Отмененных записей', default=0)
    amount = models.DecimalField(verbose_name='Общий доход', max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(verbose_name='Общий расход', max_digits=10, decimal_places=2, default=0)
    ratio = models.DecimalField(verbose_name='Соотношение', max_digits=10, decimal_places=2, default=0)
    clients = models.IntegerField(verbose_name='Всего клиентов', default=0)
    avg_cheque = models.DecimalField(verbose_name='Средний чек', max_digits=10, decimal_places=2, default=0)
    stocks = models.DecimalField(verbose_name='Скидок на сумму', max_digits=10, decimal_places=2, default=0)
    amount_stocks = models.DecimalField(verbose_name='Доход с учетом скидок', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"

    def __str__(self):
        return "%s %s %s %s %s %s" % (
            self.finished, self.canceled, self.amount, self.expense, self.ratio, self.amount_stocks
        )


@receiver(post_save, sender=Appointment)
def create_report_with_count(sender, instance, created, **kwargs):
    finished_appointments = Appointment.objects.filter(status='Завершен')
    finished = len(finished_appointments)
    canceled_appointments = Appointment.objects.filter(status='Отменен')
    canceled = len(canceled_appointments)

    amount = 0
    if instance.status == 'Завершен':
        amount += instance.total_price

    income = Income.get_solo()
    if instance.status == 'Завершен':
        income.finished = finished
    if instance.status == 'Отменен':
        income.canceled = canceled
    income.amount += amount
    income.ratio = income.amount - income.expense - income.stocks
    income.amount_stocks = income.amount - income.stocks
    try:
        income.avg_cheque = float(income.amount) / float(income.finished)
    except ZeroDivisionError:
        print("Division by 0")
    income.save()


@receiver(post_save, sender=Expense)
def add_expense_to_report(sender, instance, created, **kwargs):
    income = Income.get_solo()
    income.expense += instance.price
    income.ratio = income.amount - income.expense
    income.save()


@receiver(post_save, sender=Client)
def count_new_clients(sender, instance, created, **kwargs):
    clients = Client.objects.count()
    income = Income.get_solo()
    income.clients = clients
    income.save()


@receiver(post_save, sender=Cheque)
def count_stock_amount(sender, instance, created, **kwargs):
    income = Income.get_solo()
    stocks = 0
    if instance.stock:
        price = instance.price
        amount = instance.amount
        stocks += float(price) - float(amount)
    income.stocks += Decimal(stocks)
    income.save()


class DailyReport(models.Model):
    finished = models.IntegerField(verbose_name='Завершенных записей', default=0)
    canceled = models.IntegerField(verbose_name='Отмененных записей', default=0)
    amount = models.DecimalField(verbose_name='Общий доход', max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(verbose_name='Общий расход', max_digits=10, decimal_places=2, default=0)
    ratio = models.DecimalField(verbose_name='Соотношение доход/расход', max_digits=10, decimal_places=2, default=0)
    avg_cheque = models.DecimalField(verbose_name='Средний чек', max_digits=10, decimal_places=2, default=0)
    clients = models.IntegerField(verbose_name='Новых клиентов', default=0)
    stocks = models.DecimalField(verbose_name='Скидок на сумму', max_digits=10, decimal_places=2, default=0)
    amount_stocks = models.DecimalField(verbose_name='Доход с учетом скидок', max_digits=10, decimal_places=2,
                                        default=0)
    date = models.DateField(verbose_name='Дата отчета', auto_now=True)

    class Meta:
        verbose_name = 'Отчет за день'
        verbose_name_plural = 'Отчеты по дням'


@receiver(post_save, sender=Appointment)
def create_daily_report_with_count(sender, instance, created, **kwargs):
    finished_appointments = Appointment.objects.filter(status='Завершен')
    finished = len(finished_appointments)
    canceled_appointments = Appointment.objects.filter(status='Отменен')
    canceled = len(canceled_appointments)
    today = datetime.now().date()

    amount = 0
    if instance.status == 'Завершен' and instance.date == today:
        amount += instance.service.price

    report_day = DailyReport.objects.values('date')
    print(today)
    if report_day != today:
        if created:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.date == today:
                if instance.status == 'Завершен':
                    finished = Appointment.objects.filter(date=today).count()
                    report.finished = finished
                if instance.status == 'Отменен':
                    canceled = Appointment.objects.filter(date=today).count()
                    report.canceled = canceled
            report.amount += amount
            report.ratio = report.amount - report.expense
            report.amount_stocks = report.amount - report.stocks
            try:
                report.avg_cheque = float(report.amount) / float(report.finished)
            except ZeroDivisionError:
                print("Division by 0")
            report.save()


@receiver(post_save, sender=Expense)
def add_expense_to_daily_report(sender, instance, created, **kwargs):
    today = datetime.now().date()
    report_day = DailyReport.objects.values('date')
    if report_day != today:
        if created:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.date == today:
                report.expense += instance.price
                report.ratio = report.amount - report.expense
                report.save()


@receiver(post_save, sender=Client)
def count_new_clients_in_daily_report(sender, instance, created, **kwargs):
    today = datetime.now().date()
    report_day = DailyReport.objects.values('date')
    if report_day != today:
        if created:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.date == today:
                clients = Client.objects.filter(date=today).count()
                report.clients = clients
                report.save()


@receiver(post_save, sender=Cheque)
def count_stock_amount_for_daily_report(sender, instance, created, **kwargs):
    today = datetime.now().date()
    report_day = DailyReport.objects.values('date')
    stocks = 0
    if report_day != today:
        if created:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.stock and instance.date == today:
                price = instance.price
                amount = instance.amount
                stocks += float(price) - float(amount)
                report.stocks += Decimal(stocks)
                report.save()
