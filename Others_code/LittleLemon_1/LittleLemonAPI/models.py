from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255, db_index=True)
    def __str__(self) :
        return self.title

class MenuItem(models.Model):
    slug = models.SlugField(default=None)
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, db_index=True)
    featured = models.BooleanField(default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def __str__(self):
        return self.title
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=3)
    class Meta:
        unique_together = ('menuitem','user')
    def __str__(self):
        return self.menuitem.title

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=3)
    date = models.DateField(auto_now=True)
    def __str__(self):
        return self.user.username


class OrderItem(models.Model):
    order = models.ForeignKey(User,related_name="orderitem", on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=3)
    class Meta:
        unique_together = ('order', 'menuitem')
    def __str__(self):
        title = str(self.menuitem.title)
        return title