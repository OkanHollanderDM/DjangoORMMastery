from django.db import models
import uuid

from django.utils.text import slugify


class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product Types'
        verbose_name = 'Product Type'


class Product(models.Model):
    IN_STOCK = 'IS'
    OUT_OF_STOCK = 'OOS'
    BACKORDERED = 'BO'

    STOCK_STATUS = {
        IN_STOCK: 'In Stock',
        OUT_OF_STOCK: 'Out of Stock',
        BACKORDERED: 'Backorder'
    }

    pid = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=False)
    stock_status = models.CharField(max_length=3, choices=STOCK_STATUS.items(), default=OUT_OF_STOCK)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    seasonal_event = models.ForeignKey('SeasonalEvents', on_delete=models.CASCADE, null=True, blank=True)

    product_type = models.ManyToManyField('ProductType', related_name='product_type')

    class Meta:
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)


class AttributeValue(models.Model):
    value = models.CharField(max_length=100)
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE, max_length=100)


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    weights = models.FloatField(default=0.0)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    attribute_value = models.ManyToManyField('AttributeValue', related_name='attribute_value')


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField(default=0)
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name',
                            help_text='The name of the category')
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = 'Inventory Category'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class SeasonalEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class ProductLine_AttributeValue(models.Model):
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE)
    attribute_value = models.ForeignKey('AttributeValue', on_delete=models.CASCADE)


class Product_ProductType(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    product_type = models.ForeignKey('ProductType', on_delete=models.CASCADE)


class StockControl(models.Model):
    stock_qty = models.IntegerField(default=0)
    name = models.CharField(max_length=100)
    stock_product = models.OneToOneField('Product', on_delete=models.CASCADE)

