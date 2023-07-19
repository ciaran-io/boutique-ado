from django import template

register = template.Library()


@register.filter
def calculate_total_amount(price, quantity):
    return price * quantity


@register.filter
def split_word(value, delimiter):
    return value.split(delimiter)[1]
