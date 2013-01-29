from django import template

register = template.Library()

@register.filter
def percentage(decimal):
    return "%s%%" % max(1, int(round(decimal*100)))
