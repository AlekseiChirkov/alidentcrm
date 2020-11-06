from datetime import datetime
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.utils.timezone import now

from alident import settings
from .models import *


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


@receiver(post_save, sender=Appointment)
def send_email(sender, instance, created, **kwargs):
    if created:
        message = "У вас новая записть на прием, проверьте админ панель для полной информации."
        subject = "Новая запись"
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject, message, email_from, [
            'ali_dent.kg@mail.ru',
            'alidentclinic18@gmail.com',
            'tektonik_boy98@mail.ru'
        ])


@receiver(post_save, sender=Appointment)
def make_report_for_service(sender, instance, created, **kwargs):
    date = now()
    report, created = Report.objects.get_or_create(
        service_id=instance.service_id,
        date__month=date.month,
        defaults={
            'count': 1,
            'price': instance.service.price,
            'service_id': instance.service_id
        })

    if created:
        report.count += 1
        report.price += instance.service.price
        report.save()


@receiver(post_save, sender=Appointment)
def create_cheque(sender, instance, created, **kwargs):
    if instance.status == 'Завершен' and instance.is_added:
        cheque = Cheque.objects.create(
            client=instance.name + ' ' + instance.surname,
            service=instance.service,
            price=instance.service.price,
            stock=instance.stock,
            amount=instance.total_price
        )
        cheque.save()


@receiver(post_save, sender=Expense)
def add_expense_to_reports(sender, instance, created, **kwargs):
    income = Income.get_solo()
    if created:
        income.expense += instance.price
        income.ratio = income.amount - income.expense
        income.save()

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
def count_new_clients_to_reports(sender, instance, created, **kwargs):
    clients = Client.objects.count()
    income = Income.get_solo()
    income.clients = clients
    income.save()

    today = datetime.now().date()
    report_day = DailyReport.objects.values('date')
    if report_day != today:
        if created:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.date == today:
                clients = Client.objects.filter(date=today).count()
                report.clients = clients
                report.save()


@receiver(post_save, sender=Appointment)
def count_stock_amount_for_reports(sender, instance, created, **kwargs):
    today = datetime.now().date()
    report_day = DailyReport.objects.values('date')
    stocks = 0
    if report_day != today:
        if instance.is_added:
            report, created = DailyReport.objects.get_or_create(date=today)
            if instance.stock and instance.date == today:
                price = instance.service.price
                stock_price = instance.total_price
                stocks += float(price) - float(stock_price)
                report.stocks += Decimal(stocks)
                report.save()
    income = Income.get_solo()
    if instance.stock and instance.is_added:
        stock = instance.service.price - instance.total_price
        income.stocks += Decimal(stock)
        income.save()


@receiver(post_save, sender=Appointment)
def reports(sender, instance, *args, **kwargs):
    # Daily report

    today = datetime.now().date()
    finished_appointments = Appointment.objects.filter(status='Завершен', date=today)
    finished = len(finished_appointments)
    canceled_appointments = Appointment.objects.filter(status='Отменен', date=today)
    canceled = len(canceled_appointments)
    amount = 0
    if instance.is_added and instance.date == today:
        amount += instance.total_price
    report_day = DailyReport.objects.values('date')
    if report_day != today:
        if instance.is_added:
            report, created = DailyReport.objects.get_or_create(date=today)
            report.finished = finished
            report.canceled = canceled
            report.amount += amount
            report.ratio = report.amount - report.expense
            report.save()

    # Income report

    finished_appointments = Appointment.objects.filter(status='Завершен')
    finished = len(finished_appointments)
    canceled_appointments = Appointment.objects.filter(status='Отменен')
    canceled = len(canceled_appointments)

    amount = 0
    if instance.status == 'Завершен' and instance.is_added:
        amount += instance.total_price

    income = Income.get_solo()
    if instance.status == 'Завершен' and instance.is_added:
        income.finished = finished
    if instance.status == 'Отменен':
        income.canceled = canceled

    if instance.status == 'Завершен' and instance.is_added:
        income.amount += amount
        income.ratio = income.amount - income.expense
        income.amount_stocks = income.amount - income.stocks
        try:

            income.avg_cheque = float(income.amount) / float(income.finished)
        except ZeroDivisionError:
            print("Division by 0")

        income.save()
