from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import (AbstProduct, Category, Notificator, Offer, Subcategory,
                     SubcategoryProductNames, Supermarket, User, WishlistItem)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority')
    ordering = ('priority',)

class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory_link', 'priority', 'view_product_names')
    ordering = ('category', 'priority',)

    def subcategory_link(self, obj):
        url = reverse('admin:offers_subcategory_change', args=(obj.id,))
        return format_html('<a href="{}">{}</a>', url, obj.name)
    
    def product_names_link(self, obj):
        url = reverse('admin:offers_subcategory_change', args=(obj.id,))
        return format_html('<a href="{}">{}</a>', url, obj.name)

    subcategory_link.short_description = 'Subcategory'
    subcategory_link.admin_order_field = 'subcategory'

    def view_product_names(self, obj):
        url = reverse('admin:offers_subcategoryproductnames_changelist') + f'?subcategory={obj.id}'
        return format_html('<a href="{}">View</a>', url)

    view_product_names.short_description = 'product names'

admin.site.register(User)
admin.site.register(Offer)
admin.site.register(Supermarket)
admin.site.register(WishlistItem)
admin.site.register(Notificator)
admin.site.register(AbstProduct)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(SubcategoryProductNames)