from django.contrib import admin
from .models import Product
from .models import Order, Category

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Category)
# Register your models here.
