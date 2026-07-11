from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):

        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(
    Category,
    on_delete=models.CASCADE,
    null=True
    )
    def __str__(self):
        return self.name
    
class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product)

    total_price = models.IntegerField()

    address = models.TextField()

    phone = models.CharField(max_length=15)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user.username