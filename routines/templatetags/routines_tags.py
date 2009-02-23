from django import template

register = template.Library()

@register.filter
def startswith(value, arg):
    """ Usage, {% if value|starts_with:"arg" %}"""
    return value.startswith(arg)

@register.filter
def minutes_from_seconds(value, arg=False):
    value = int(value)
    mins = value / 60
    secs = value % 60
    result = ""
    from django.template.defaultfilters import pluralize
    if mins:
        result+='<span class="minutes">%d</span> minute' % mins + pluralize(mins)
    if not arg or secs:
        result+=' <span class="seconds">%d</span> second' % secs + pluralize(secs)
    from django.utils.safestring import mark_safe 
    return mark_safe(result)
