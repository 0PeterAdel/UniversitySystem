from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    """
    Add a CSS class to a form field
    """
    return value.as_widget(attrs={'class': arg})

@register.filter(name='mul')
def mul(value, arg):
    """
    Multiply the value by the argument
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0