from django import template

register = template.Library()

@register.filter
def class_name(value, class_name):
    return value.__class__.__name__ == class_name
