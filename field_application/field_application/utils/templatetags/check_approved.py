from django.template import Library

register = Library()

@register.filter
def all_approved(app_list):
    for app in app_list:
        if not app.approved:
            return False
    return True

@register.filter
def approved_exist(app_list):
    for app in app_list:
        if app.approved:
            return True
    return False

