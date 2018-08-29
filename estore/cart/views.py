from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from storeapp.models import Item
from .cart import Cart
from cart.forms import CartAddProductForm


# Create your views here.


def cart_add(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Item,id=product_id)
    cart.add(item=product)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
         cd = form.cleaned_data
         cart.add(item=product,
         quantity=cd['quantity'],
         update_quantity=cd['update'])
    return HttpResponseRedirect(reverse('storeapp:index'))

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm( initial={'quantity': item['quantity'],
                                                           'update': True})
    return render(request,'cart/cart_detail.html',{'cart':cart})

def cart_remove(request,product_id):
    cart = Cart(request)
    product = get_object_or_404(Item,id=product_id)
    cart.remove(product_id)
    return HttpResponseRedirect(reverse('cart:cart_detail'))
