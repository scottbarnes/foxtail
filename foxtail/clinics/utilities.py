""" foxtail.clinics.utilities.py """
from datetime import datetime, timedelta


# Generate the start/end range options for the clinics.
def get_time_slot_choices(start, end, delta):
    """ Generate the clinic time slots. """
    current = start
    count = 1
    slots = []
    while current < end:
        current_as_12_hour = current.strftime('%-I:%M %p')
        current_as_24_hour = current.strftime('%H:%M')
        tup = (current_as_24_hour, current_as_12_hour)
        slots.append(tup)
        count += 1
        current = start + timedelta(minutes=delta * count)
    return tuple(slots)
