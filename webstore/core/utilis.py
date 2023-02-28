import re

from django.contrib.sessions.models import Session
from django.core.exceptions import ValidationError

product_order = {
    'bestselers': '-no_of_items_sold',
    'price_a': 'current_price',
    'price_d': '-current_price',
}


def total_amount_for_session(queryset):
    total = 0
    for cart in queryset:
        total += cart.total()
    return total

def validate_postcode(postcode):
    regex = re.compile("[0-9]{2}-[0-9]{3}")
    if regex.match(str(postcode)):
        return postcode
    else:
        raise ValidationError("Wrong post code format!")

def validate_discount(amount):
    regex_percent = re.compile("([0-9]%)|([1-9][0-9]%)")

    if regex_percent.match(str(amount)) or str(amount).isdigit():
        return amount
    else:
        raise ValidationError("Wrong amount format!")
