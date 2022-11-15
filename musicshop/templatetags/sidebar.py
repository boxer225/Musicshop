from django import template
from musicshop.models import Category
from django.db.models import Count, F

register = template.Library()

@register.inclusion_tag('musicshop/sidebar_tpl.html')
def show_sidebar():
    categories = Category.objects.all()
    rod = categories.get_ancestors().filter(level=0)
    return {'parents': rod}