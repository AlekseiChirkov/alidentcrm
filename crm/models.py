from django.db import models
from solo.models import SingletonModel
from django.db.models import Count, Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import MyUser


class Staff(models.Model):
    name = models.CharField(verbose_name='Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name='Телефон', max_length=16)
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField()

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=MyUser)
def make_doctor(sender, instance, created, **kwargs):
    if instance.category == 'Персонал':
        staff = Staff.objects.create(
            name=instance.name + ' ' + instance.surname + ' ' + instance.patronymic,
            phone=instance.username,
            birthday=instance.birthday,
            email=instance.email
        )
        print(staff.name)
        staff.save()


class Client(models.Model):
    name = models.CharField(verbose_name='Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name='Телефон', max_length=16)
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField()

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return str(self.name)


@receiver(post_save, sender=MyUser)
def make_client(sender, instance, created, **kwargs):
    if instance.category == 'Клиент':
        client = Client.objects.create(
            name=instance.name + ' ' + instance.surname + ' ' + instance.patronymic,
            phone=instance.username,
            birthday=instance.birthday,
            email=instance.email
        )
        print(client.name)
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
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE, default=None)
    percentage = models.IntegerField(verbose_name='Скидка в %')

    class Meta:
        verbose_name = "Акция"
        verbose_name_plural = "Акции"

    def __str__(self):
        return '%s %s' % (self.service, self.percentage)


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
    status = models.CharField(verbose_name='Статус', max_length=64, choices=STATUS_CHOICES)
    appointment_income = models.ForeignKey('Income', verbose_name='Доход с записи', on_delete=models.CASCADE,
                                           default=None, null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return '%s %s %s' % (
            self.name, self.surname, self.time
        )

    def save(self, *args, **kwargs):
        price = self.service.price
        self.total_price = price
        super(Appointment, self).save(*args, **kwargs)


class Expense(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    category = models.CharField(verbose_name='Категория расхода', max_length=64)
    description = models.CharField(verbose_name='Описание', max_length=128)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость (сом)', max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name='Дата')

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
    qs = Appointment.objects.values('service', 'service__report__date').\
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


class Income(SingletonModel):
    finished = models.IntegerField(verbose_name='Завершенных записей', default=0)
    canceled = models.IntegerField(verbose_name='Отмененных записей', default=0)
    amount = models.DecimalField(verbose_name='Общий доход', max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(verbose_name='Общий расход', max_digits=10, decimal_places=2, default=0)
    ratio = models.DecimalField(verbose_name='Соотношение', max_digits=10, decimal_places=2, default=0)
    clients = models.IntegerField(verbose_name='Всего клиентов', default=0)

    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"

    def __str__(self):
        return "%s %s %s %s %s" % (
            self.finished, self.canceled, self.amount, self.expense, self.ratio
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
        income.finished += finished
    if instance.status == 'Отменен':
        income.canceled += canceled
    income.amount += amount
    income.ratio = income.amount - income.expense
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
    print(clients)
    income = Income.get_solo()
    income.clients = clients
    income.save()
