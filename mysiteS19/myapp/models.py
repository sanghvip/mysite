from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

#category model for defing categories
class Category(models.Model):
    name = models.CharField(max_length=200)
    warehouse=models.CharField(max_length=100,default="Windsor")

    class Meta:
        ordering = ['id'] 
    def __str__(self):
        return (self.name)

#product detail model
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=100)
    available = models.BooleanField(default=True)
    intrested = models.PositiveIntegerField(default=0)
    description=models.TextField(max_length=500,blank=True,default='')

    def refill(self):
        self.stock+=100

    class Meta:
        ordering = ['id'] 

    def __str__(self):
        return '{} {} {} {} {} {}'.format(self.name,self.category.name,self.price,self.stock,self.available,self.description)

#user detail for order
class Client(User):
    PROVINCE_CHOICES = [('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'),('QC', 'Quebec'), ]
    company = models.CharField(max_length=50,blank=True,default='')
    shipping_address = models.CharField(max_length=300, null=True, blank=True)
    city = models.CharField(max_length=20,default="Windsor")
    province = models.CharField(max_length=2, choices=PROVINCE_CHOICES, default='ON')
    interested_in = models.ManyToManyField(Category)

    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return '{} {}'.format(self.first_name,self.last_name)

#fOrder Model for user's
class Order(models.Model):
    product=models.ForeignKey(Product,related_name="products",on_delete=models.CASCADE)
    client=models.ForeignKey(Client,related_name="clients",on_delete=models.CASCADE)
    num_units=models.PositiveIntegerField(default=100)
    status_choices=[(0,'Order Cancelled'),(1, 'Order Placed'),(2, 'Order Shipped'),(3, 'Order Delivered')]
    order_status = models.IntegerField(choices=status_choices,default=1)
    status_date=models.DateField(("Date"), default=datetime.date.today)

    class Meta:
        ordering = ['id']

    def total_cost(self):
        return self.num_units * self.product.price
        
    def __str__(self):
        return '{} {} {} {} {}'.format(self.product.name,self.client.first_name,self.client.last_name,self.num_units,self.order_status,self.status_date)
    
    

