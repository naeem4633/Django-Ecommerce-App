from django.db import models

# Create your models here.
class Product(models.Model):
    sku = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartItems', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    is_wishlist_item = models.BooleanField(default=False, null=True, blank=True)

class Order(models.Model):
    cartItem = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    order_status = models.CharField(max_length=100)
