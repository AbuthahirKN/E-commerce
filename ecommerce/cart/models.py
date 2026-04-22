from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

# Create your models here.
class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity= models.IntegerField(default=0)
    date_added =  models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.product.price
    def __str__(self):
        return self.user.username
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField(null=True)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=100,null=True)
    payment_method =models.CharField(max_length=100,null=True)
    address = models.TextField(null=True)
    phone = models.CharField(max_length=16,null=True)
    is_ordered =models.BooleanField(default=False)
    delivery_status = models.CharField(default='pending',max_length=100,null=True)

    def __str__(self):
        return self.user.username

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return str(self.order.order_id)









