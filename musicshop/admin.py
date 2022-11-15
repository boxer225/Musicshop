from django.contrib import admin
from .models import *
from .forms import RegisterForm
from mptt.admin import DraggableMPTTAdmin
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin


class CatalogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name', 'slug', 'price', 'category', 'get_photo', 'count')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('category', 'city')
    save_on_top = True
    save_as = True
    readonly_fields = ('get_photo',)
    fields = ('name', 'slug', 'description', 'price', 'category', 'city', 'count', 'image', 'comment')


    def get_photo(self, object):
        if object.image:
            return mark_safe(f'<img src="{object.image.url}" width=50">')
        return '-'

    get_photo.short_description = 'Фото'


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'address',)
    list_display_links = ('id',)
    search_fields = ('city',)
    list_filter = ('city',)
    save_on_top = True
    save_as = True
    fields = ('city', 'address',)

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = RegisterForm

    list_display = ('username', 'fio', 'email', 'number_of_phone')
    list_display_links = ('username', 'email')
    search_fields = ('username', 'fio', 'email')
    save_on_top = True
    save_as = True
    fieldsets = (
        (None, {'fields': ('username', 'fio', 'email',  'number_of_phone')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
    ),
    list_display_links=(
        'indented_title',
    ),
)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Shop, ShopAdmin)