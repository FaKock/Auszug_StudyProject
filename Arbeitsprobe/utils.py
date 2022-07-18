import datetime

# converts the duration string into a datetime.timedelta object
def parse_duration(value):

    # since our widget inherits from time input, the value for creating a task would be a datetime object,
    # while after saving it is a string
    # to treat both versions the same, the value is converted first
    duration_str = str(value)
    minutes = int(duration_str[3] + duration_str[4])
    hours = int(duration_str[0] + duration_str[1])
    seconds = minutes * 60 + hours * 3600  # needs to be converted because timedelta is saved in seconds

    return datetime.timedelta(days=0, seconds=seconds, microseconds=0)