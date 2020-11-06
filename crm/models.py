from django.db import models
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
        verbose_name = "Люди - Персонал"
        verbose_name_plural = "Люди - Персонал"

    def __str__(self):
        return str(self.name)


class Client(models.Model):
    name = models.CharField(verbose_name='Ф.И.О.', max_length=128)
    phone = models.CharField(verbose_name='Телефон', max_length=16)
    birthday = models.DateField(verbose_name='Дата рождения')
    email = models.EmailField(blank=True, null=True)
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Люди - Клиент"
        verbose_name_plural = "Люди - Клиенты"

    def __str__(self):
        return str(self.name)


class ServiceCategory(models.Model):
    name = models.CharField(verbose_name='Название', max_length=128)

    class Meta:
        verbose_name = "Услуги - Категория"
        verbose_name_plural = "Услуги - Категории"

    def __str__(self):
        return self.name


class Service(models.Model):
    code = models.CharField(verbose_name='Кодировка', max_length=32)
    name = models.CharField(verbose_name='Услуга', max_length=128)
    category = models.ForeignKey(ServiceCategory, verbose_name='Категория', on_delete=models.CASCADE, default=None)
    price = models.DecimalField(verbose_name='Цена', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Услуги - Услуга"
        verbose_name_plural = "Услуги - Услуги"

    def __str__(self):
        return f"{self.code}, {self.name}, {self.price} сом"


class Stock(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=64)
    description = models.CharField(verbose_name='Описание', max_length=256)
    percentage = models.IntegerField(verbose_name='Скидка в %')
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Услуги - Акция"
        verbose_name_plural = "Услуги - Акции"

    def __str__(self):
        return '%s' % self.percentage


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
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE,
                                default=None, null=True, blank=True)
    service_title = models.CharField(verbose_name='Описание врача', max_length=256, blank=True, null=True)
    stock = models.ForeignKey(Stock, verbose_name='Акция', on_delete=models.CASCADE,
                              default=None, blank=True, null=True)
    date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    is_added = models.BooleanField(verbose_name='Добавлено в отчет', default=False)

    class Meta:
        verbose_name = "Записи - Запись на прием"
        verbose_name_plural = "Записи - Записи на прием"

    def __str__(self):
        return '%s %s %s' % (
            self.name, self.surname, self.time
        )

    def save(self, *args, **kwargs):
        if self.service:
            price = self.service.price
            if self.stock:
                stock = self.stock.percentage * 0.01
                stock_price = Decimal(price) - Decimal(price) * Decimal(stock)
                self.total_price = Decimal(stock_price)
            else:
                self.total_price = price
        if self.status == 'Завершен' and not self.is_added:
            self.is_added = True
        super(Appointment, self).save(*args, **kwargs)


class Expense(models.Model):
    name = models.CharField(verbose_name='Название', max_length=64)
    category = models.CharField(verbose_name='Категория расхода', max_length=64)
    description = models.CharField(verbose_name='Описание', max_length=128)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name='Стоимость (сом)', max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name='Дата создания', auto_now=True)

    class Meta:
        verbose_name = "Отчеты - Расход"
        verbose_name_plural = "Отчеты - Расходы"

    def __str__(self):
        return '%s %s %s %s %s %s' % (
            self.name, self.category, self.description, self.service, self.price, self.date
        )


class Report(models.Model):
    service = models.ForeignKey(Service, verbose_name='Название услуги', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='Записей за месяц')
    price = models.DecimalField(verbose_name='Сумма', max_digits=10, decimal_places=2)
    date = models.DateField(verbose_name='Дата отчета', auto_now_add=True)

    class Meta:
        verbose_name = "Отчеты - Услуга"
        verbose_name_plural = "Отчеты - Услуги"

    def __str__(self):
        return '%s %s %s %s' % (self.service, self.count, self.price, self.date)


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
        verbose_name = 'Записи - Чек за прием'
        verbose_name_plural = 'Записи - Чеки за прием'

    def save(self, *args, **kwargs):
        if self.stock:
            stock_value = self.stock.percentage * 0.01
            stock = float(self.price) * stock_value
            amount = float(self.price) - stock
            self.amount = amount
        else:
            self.amount = self.price
        super(Cheque, self).save(*args, **kwargs)


class Income(SingletonModel):
    finished = models.IntegerField(verbose_name='Завершенных записей', default=0)
    canceled = models.IntegerField(verbose_name='Отмененных записей', default=0)
    amount = models.DecimalField(verbose_name='Общий доход', max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(verbose_name='Общий расход', max_digits=10, decimal_places=2, default=0)
    ratio = models.DecimalField(verbose_name='Чистая прибыль', max_digits=10, decimal_places=2, default=0)
    clients = models.IntegerField(verbose_name='Всего клиентов', default=0)
    avg_cheque = models.DecimalField(verbose_name='Средний чек', max_digits=10, decimal_places=2, default=0)
    stocks = models.DecimalField(verbose_name='Скидок на сумму', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Отчеты - Доход"
        verbose_name_plural = "Отчеты - Доходы"

    def __str__(self):
        return "%s %s %s %s %s %s" % (
            self.finished, self.canceled, self.amount, self.expense, self.ratio, self.amount_stocks
        )


class DailyReport(models.Model):
    finished = models.IntegerField(verbose_name='Завершенных записей', default=0)
    canceled = models.IntegerField(verbose_name='Отмененных записей', default=0)
    amount = models.DecimalField(verbose_name='Общий доход', max_digits=10, decimal_places=2, default=0)
    expense = models.DecimalField(verbose_name='Общий расход', max_digits=10, decimal_places=2, default=0)
    ratio = models.DecimalField(verbose_name='Чистая прибыль', max_digits=10, decimal_places=2, default=0)
    avg_cheque = models.DecimalField(verbose_name='Средний чек', max_digits=10, decimal_places=2, default=0)
    clients = models.IntegerField(verbose_name='Новых клиентов', default=0)
    stocks = models.DecimalField(verbose_name='Скидок на сумму', max_digits=10, decimal_places=2, default=0)
    date = models.DateField(verbose_name='Дата отчета', auto_now=True)

    class Meta:
        verbose_name = 'Отчеты - Отчет за день'
        verbose_name_plural = 'Отчеты - Отчеты по дням'



