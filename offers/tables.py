import django_tables2 as tables
from django.utils.safestring import mark_safe

from .models import Offer


class ItemTable(tables.Table):
    product_img_local = tables.TemplateColumn(template_name='offers/table_images_column.html', verbose_name='Image', orderable=True)
    category = tables.TemplateColumn(template_name='offers/table_category_column.html', verbose_name='Category', orderable=True)
    subcategory = tables.TemplateColumn(template_name='offers/table_subcategory_column.html', verbose_name='Subcategory', orderable=True)
    # product_name = tables.Column(verbose_name='Product Name', empty_values=())
    product_name = tables.LinkColumn('offers:offer-update', args=[tables.A('pk')], verbose_name='Product Name', empty_values=())

    def render_product_name(self, value, record):
        # Add the product ID as an attribute to the <td> element
        return mark_safe(f'<span class="product_name" offer-id="{record.id}">{value}</span>')

    class Meta:
        model = Offer
        fields = ('product_img_local', 'product_name', 'category', 'subcategory', 'created_on', 'supermarket')
        attrs = {
            'td': {'class': 'px-4 py-3'},
            'th': {'class': 'px-4 py-3 title-font tracking-wider font-medium text-gray-900 text-sm bg-gray-100'},
            'class': 'table-auto w-full text-left whitespace-no-wrap',
        }
