from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm 
# Create your models here.


class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
    
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()

    def __str__(self):
        return self.description

class ShopCart(models.Model):
    user=models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    product=models.ForeignKey(Photo,on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField()
    

    def __str__(self):
        return self.product.title
    @property
    def price(self):
        return(self.product.price)
    