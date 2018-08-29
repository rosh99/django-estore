from django.contrib import admin
from .models import Categories,Brand,Item,UserInfo,Order
# Register your models here.


admin.site.register(Item)
admin.site.register(Categories)
admin.site.register(Brand)
admin.site.register(UserInfo)
admin.site.register(Order)
