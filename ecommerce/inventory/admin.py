from django.contrib import admin

from .models import (
    Attribute,
    AttributeValue,
    Category,
    Product,
    ProductImage,
    ProductLine,
    ProductType,
    SeasonalEvent,
)


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


class ProductLineInline(admin.StackedInline):
    model = ProductLine
    inlines = [ProductImageInline]
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductLineInline]

    list_display = (
        "name",
        "category",
        "stock_status",
        "is_active",
    )

    list_filter = (
        "category",
        "stock_status",
        "is_active",
    )

    search_fields = ("name",)


class SeasonalEventAdmin(admin.ModelAdmin):
    list_display = ("name", "start_date", "end_date")


class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1


class AttributeAdmin(admin.ModelAdmin):
    inlines = [AttributeValueInline]


class ChildTypeInline(admin.TabularInline):
    model = ProductType
    fk_name = "parent"
    extra = 1


class ParentTypeAdmin(admin.ModelAdmin):
    inlines = [ChildTypeInline]


class ChildCategoryInline(admin.TabularInline):
    model = Category
    fk_name = "parent"
    extra = 1


class ParentCategoryAdmin(admin.ModelAdmin):
    inlines = [ChildCategoryInline]
    list_display = (
        "name",
        "parent_name",
    )

    def parent_name(self, obj):
        return obj.parent.name if obj.parent else None


admin.site.register(Product, ProductAdmin)
admin.site.register(SeasonalEvent, SeasonalEventAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(ProductType, ParentTypeAdmin)
admin.site.register(Category, ParentCategoryAdmin)
