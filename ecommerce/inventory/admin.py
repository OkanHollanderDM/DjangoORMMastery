from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Category, Product, ProductType, ProductLine


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'slug']
    list_display = ['id', 'name', 'slug', 'is_active']
    list_editable = ['is_active']
    list_display_links = ['id']


class ProductLineInLine(admin.StackedInline):
    model = ProductLine
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['id', 'name', 'category_link', 'is_active', 'is_digital', 'stock_status']
    list_editable = ['is_active', 'is_digital', 'stock_status']
    list_display_links = ['id']
    search_fields = ['name', 'stock_status']
    list_filter = ['stock_status']

    def category_link(self, obj):
        link = reverse('admin:inventory_category_change', args=[obj.category.id])
        return format_html('<a href="{}">{}</a>', link, obj.category.name)

    category_link.short_description = 'Category'

    inlines = [ProductLineInLine]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductType)

