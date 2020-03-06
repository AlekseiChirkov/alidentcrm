from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import MyUser


class Staff(models.Model):
    staff = models.ForeignKey(MyUser, verbose_name='Персонал', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = "Персонал"
        verbose_name_plural = "Персонал"

    def __str__(self):
        return str(self.staff)


class ServiceCategory(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Service(models.Model):
    code = models.FloatField(verbose_name='Кодировка')
    name = models.CharField(verbose_name='Услуга', max_length=128)
    category = models.ForeignKey(ServiceCategory, verbose_name='Категория',  on_delete=models.CASCADE, default=None)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


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


class Stage(models.Model):
    status = models.CharField(verbose_name="Статус", max_length=64)

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

    def __str__(self):
        return self.status


class Appointment(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=64)
    surname = models.CharField(verbose_name='Фамилия', max_length=64)
    time = models.DateTimeField(verbose_name='Время')
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2, default=0)
    status = models.ForeignKey(Stage, verbose_name='Статус', on_delete=models.CASCADE, default=None)
    appointment_income = models.ForeignKey('Income', verbose_name='Доход с записи', on_delete=models.CASCADE,
                                           default=None, null=True, blank=True)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE, default=None)

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return '%s %s %s %s' % (
            self.name, self.surname, self.time, self.time
        )


class Income(models.Model):
    cheque = models.ForeignKey(Appointment, verbose_name='Чек', on_delete=models.CASCADE, default=None, null=True, blank=True)
    date = models.DateField(verbose_name='Дата', auto_now_add=True)
    total_income = models.DecimalField(verbose_name='Доход', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Доход"
        verbose_name_plural = "Доходы"

    def __str__(self):
        return "%s %s" % (self.date, self.total_income)


@receiver(post_save, sender=Appointment)
def income_adder(sender, instance, created, **kwargs):
    # if created:
    income, created = Income.objects.get_or_create()
    income.total_income += instance.total_price
    print(income.total_income)
    income.save()


class Cheque(models.Model):
    appointment = models.ForeignKey(Appointment, verbose_name='Запись', on_delete=models.CASCADE, default=None)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE, default=None)
    count = models.IntegerField(verbose_name='Количество', default=1)
    price_per = models.DecimalField(verbose_name='Цена за одну услугу', max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(verbose_name='Всего', max_digits=10, decimal_places=2, default=0)
    stock = models.ForeignKey(Stock, verbose_name='Акция', on_delete=models.CASCADE, default=None, null=True, blank=True)

    class Meta:
        verbose_name = "Чек"
        verbose_name_plural = "Чеки"

    def __str__(self):
        return self.service.name

    def save(self, *args, **kwargs):
        price_per_serv = self.service.price
        self.price_per = price_per_serv
        self.total_price = self.count * price_per_serv
        if self.stock:
            discount = float(self.stock.percentage) * 0.01
            percentage = float(self.total_price) * discount
            self.total_price = float(self.total_price) - percentage

        super(Cheque, self).save(*args, **kwargs)


def service_post_save(sender, instance, created, **kwargs):
    appointment = instance.appointment
    all_services = Cheque.objects.filter(appointment=appointment)

    appointment_total_price = 0
    for item in all_services:
        appointment_total_price += item.total_price

    instance.appointment.total_price = appointment_total_price
    instance.appointment.save(force_update=True)


post_save.connect(service_post_save, sender=Cheque)


class Expense(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    expense_category = models.CharField(verbose_name='Категория расхода', max_length=64)
    description = models.TextField(verbose_name='Примечания', max_length=512)
    price = models.DecimalField(verbose_name='Стоимость', max_digits=10, decimal_places=2)
    service = models.ManyToManyField(Service, verbose_name='Услуга', default=None)
    date = models.DateField()

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"

    def __str__(self):
        return '%s %s %s %s %s' % (self.name, self.description, self.price, self.service, self.date)

