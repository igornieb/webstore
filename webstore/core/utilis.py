from django.contrib.sessions.models import Session

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
