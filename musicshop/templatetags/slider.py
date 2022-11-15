from django import template
from musicshop.models import Category

register = template.Library()

@register.inclusion_tag('musicshop/slider_tpl.html')
def show_slider():
    categories = Category.objects.all()
    rod = categories.get_ancestors().filter(level=0)[:2]
    return {'parents': rod}