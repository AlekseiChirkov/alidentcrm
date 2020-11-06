from django import forms

from .models import *

STATUS_CHOICES = [
    ('Активен', 'Активен'),
    ('Завершен', 'Завершен'),
    ('Приостановлен', 'Приостановлен'),
    ('Отменен', 'Отменен')
]


class AppointmentForm(forms.ModelForm):
    time = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1'
        })
    )

    class Meta:
        model = Appointment
        fields = ['name', 'surname', 'phone',
                  'time', 'doctor']

    def save(self, commit=True):
        appointment = super().save(commit=False)
        if commit:
            appointment.save()
        return appointment
