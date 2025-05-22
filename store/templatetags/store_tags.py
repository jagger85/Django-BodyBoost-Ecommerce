from django import template

register = template.Library()

@register.filter
def get_min_price(product):
    variants = product.variant.all()
    if variants:
        return min(variant.price for variant in variants)
    return 0

@register.filter
def get_first_variant_id(product):
    variant = product.variant.first()
    return variant.id if variant else None