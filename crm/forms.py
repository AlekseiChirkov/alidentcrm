from django import forms

from .models import *

STATUS_CHOICES = [
    ('Активен', 'Активен'),
    ('Завершен', 'Завершен'),
    ('Приостановлен', 'Приостановлен'),
    ('Отменен', 'Отменен')
]


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'phone',
                  'time', 'service', 'doctor']

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if commit:
            appointment.save()
        return appointment
