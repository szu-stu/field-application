import datetime, timedelta
import calendar


def generate_current_month_table():
    calendar = calendar.Calendar()
    month_table = {}
    month_table['date'] = []
    for date in calendar.itermonthdates():
        month_table['date'].append(date)
    return month_table


