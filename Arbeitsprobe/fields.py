import datetime
from django.db.models import fields
from django import forms
from django.core import exceptions
from .utils import parse_duration


# customizing the duration model field so that it uses our parsing function
# the functions can be used from the original DurationField code
class CustomDurationModelField(fields.DurationField):

    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, datetime.timedelta):
            return value
        try:
            parsed = parse_duration(value)
        except ValueError:
            pass
        else:
            if parsed is not None:
                return parsed

        raise exceptions.ValidationError(
            self.error_messages['invalid'],
            code='invalid',
            params={'value': value},
        )

    # model fields inherit from the form fields
    # since the parsing function is used there as well, this is customized too and needs to be changed here
    def formfield(self, **kwargs):
        return super().formfield(**{
            'form_class': CustomDurationFormField,
            **kwargs,
        })


# customizing the duration form field so that it uses our parsing function
class CustomDurationFormField(forms.DurationField):

    def to_python(self, value):
        if value in self.empty_values:
            return None
        if isinstance(value, datetime.timedelta):
            return value
        try:
            value = parse_duration(str(value))
        except OverflowError:
            raise exceptions.ValidationError(self.error_messages['overflow'].format(
                min_days=datetime.timedelta.min.days,
                max_days=datetime.timedelta.max.days,
            ), code='overflow')
        if value is None:
            raise exceptions.ValidationError(self.error_messages['invalid'], code='invalid')
        return value