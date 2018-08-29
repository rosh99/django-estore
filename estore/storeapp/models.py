from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.



class Categories(models.Model):
    cat_name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True,default='cat-slug')
    def __str__(self):
        return self.cat_name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.cat_name)
        super().save(*args,**kwargs)

class Brand(models.Model):
    brand_name = models.CharField(max_length=200)
    category = models.ForeignKey(Categories,related_name='brand',on_delete='CASCADE')
    slug = models.SlugField(allow_unicode=True,default='brand-slug')

    def __str__(self):
        return self.brand_name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.brand_name)
        super().save(*args,**kwargs)

class Item(models.Model):
    brand = models.ForeignKey(Brand,related_name='item',on_delete='CASCADE')
    item_name = models.CharField(max_length=200)
    slug = models.SlugField(allow_unicode=True,default='item-name')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    image = models.ImageField(upload_to='pictures',null=True)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        self.slug = slugify(self.item_name)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.item_name


class UserInfo(models.Model):
    user = models.OneToOneField(User,on_delete='CASCADE',related_name='userinfo')
    city = models.CharField(max_length=200)
    house = models.CharField(max_length=200)
    def __str__(self):
        return self.user.username

class Order(models.Model):
    user = models.ForeignKey(UserInfo,on_delete='CASCADE',related_name='order')
    product = models.ForeignKey(Item,on_delete='CASCADE',related_name='product')
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return  'Order {}'.format(self.id)
