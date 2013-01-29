from django import template

register = template.Library()

@register.filter
def percentage(decimal):
    return "%s%%" % int(round(decimal*100))
