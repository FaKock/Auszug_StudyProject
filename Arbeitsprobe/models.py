import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from .fields import CustomDurationModelField


class Task(models.Model):

    # add choice options hard coded only if no new options should be added
    class Priority(models.IntegerChoices):
        HIGH = (3, 'high')
        MEDIUM = (2, 'medium')
        LOW = (1, 'low')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    title = models.CharField(max_length=100)
    deadline_date = models.DateField()
    deadline_time = models.TimeField()
    duration = CustomDurationModelField()
    # integer choice field makes interpolation later on possible
    priority = models.IntegerField(choices=Priority.choices, default=Priority.LOW)
    description = models.TextField(max_length=2000, blank=True, null=True)
    # bool to enable easy check of completion
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} until {self.deadline_date}, {self.deadline_time}'
