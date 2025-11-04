from django import template

register = template.Library()

@register.filter
def split_comma(value):
    """Split a string by comma"""
    if value:
        return [item.strip() for item in value.split(',')]
    return []
