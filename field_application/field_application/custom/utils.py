from datetime import datetime, timedelta

from django.utils import timezone


def generate_date_list_this_week():
    date_list = []
    now = timezone.now()
    date_of_this_Monday = now - timedelta(days=now.weekday())
    for i in range(0, 7):
        date_list.append(date_of_this_Monday + timedelta(days=i))
    return date_list
