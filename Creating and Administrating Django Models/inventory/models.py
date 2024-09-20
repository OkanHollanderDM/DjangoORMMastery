from django.db import models
import uuid


class Product(models.Model):
    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)


class ProductLine(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.UUIDField(default=uuid.uuid4, editable=False)
    stock_qty = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    weight - models.FloatField(default=0.0)


class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    is_active = models.BooleanField(default=True)


class SeasonalEvents(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
