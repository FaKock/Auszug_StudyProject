from django.forms import widgets, Widget
from .utils import parse_duration


class CustomDurationInput(widgets.TimeInput):

    @staticmethod
    def format_value(value, **kwargs):
        # this method can be used for every different input widget to customize the displayed format

        # is needed for the test function because it doesn't use the initial value and is therefore None
        if value is None:
            return '00:30'

        duration = parse_duration(value)  # returns a datetime.timedelta object

        seconds = duration.seconds  # datetime.timedelta objects only have days, seconds and microseconds
        minutes = seconds // 60
        hours = minutes // 60
        minutes = minutes % 60

        return '{:02d}:{:02d}'.format(hours, minutes)

