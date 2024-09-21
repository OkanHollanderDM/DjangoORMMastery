from django.db import models
import uuid


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
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    seasonal_event = models.ForeignKey('SeasonalEvents', on_delete=models.CASCADE)


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    weight - models.FloatField(default=0.0)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField(default=0)
    product_line = models.ForeignKey('ProductLine', on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)


class SeasonalEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
