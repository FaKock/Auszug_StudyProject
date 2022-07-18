from django import forms
from django.forms import ModelForm
from .models import Task
from .widgets import CustomDurationInput
from django.core.exceptions import ValidationError
import datetime

class TaskForm(ModelForm):

    # insert clean functions here if needed (see also in views.py forms.is_invalid() for TaskCreate)

    # clean_<field-name> functions can be used to raise validation errors if an input is not valid
    def clean_deadline_time(self):
        # normally use the cleaned data but not here because this will contradict the clean_deadline_date function
        deadline_date = self.data.get('deadline_date')
        # here use the cleaned data again
        deadline_time = self.cleaned_data['deadline_time']

        if (str(deadline_date) == str(datetime.date.today())) & (deadline_time < datetime.datetime.now().time()):
            raise ValidationError('Time is in the past', code='invalid')

        return deadline_time

    def clean_deadline_date(self):
        deadline_date = self.cleaned_data['deadline_date']

        if deadline_date < datetime.date.today():
            raise ValidationError('Date is in the past', code='invalid')

        return deadline_date

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if duration.total_seconds() < 300:  # smaller than 5 minutes
            raise ValidationError('Duration is too small', code='invalid')

        return duration

    class Meta:
        model = Task
        fields = ('title', 'deadline_date', 'deadline_time',
                  'duration', 'priority', 'description', 'complete')

        widgets = {
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'New task',
                    'class': 'widget-inputs widget-title',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Description',
                    'class': 'widget-inputs widget-description'
                }
            ),
            'deadline_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'widget-inputs widget-time-fields active'
                }
            ),
            'deadline_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'widget-inputs widget-time-fields active'
                },
                format='%H:%M'
            ),
            'duration': CustomDurationInput(
                attrs={
                    'type': 'time',
                    'class': 'widget-inputs widget-duration'
                }
            ),
            'priority': forms.Select(
                attrs={
                    'class': 'widget-inputs widget-category'
                }
            ),
        }



