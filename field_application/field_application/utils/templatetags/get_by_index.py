from django.template import Library

register = Library()

@register.filter
def get(iterator, index):
    return iterator[index]
