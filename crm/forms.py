from django import forms

from .models import *

STATUS_CHOICES = [
    ('Активен', 'Активен'),
    ('Завершен', 'Завершен'),
    ('Приостановлен', 'Приостановлен'),
    ('Отменен', 'Отменен')
]


class AppointmentForm(forms.ModelForm):
    # name = forms.CharField(label='Имя')
    # surname = forms.CharField(label='Фамилия')
    # phone = forms.CharField(label='Телефон')
    # time = forms.DateTimeField(label='Время', help_text='Формат даты: 2020-12-31 18:00')
    # service = forms.ModelChoiceField(label='Услуга', queryset=Service.objects.all())
    # status = forms.ChoiceField(label='Статус', choices=STATUS_CHOICES)
    # doctor = forms.ModelChoiceField(label='Врач', queryset=Staff.objects.all())

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'phone',
                  'time', 'service', 'doctor']

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if commit:
            appointment.save()
        return appointment
