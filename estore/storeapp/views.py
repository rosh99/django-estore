from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate,login
from django.urls import reverse
from django.contrib.auth.models import User
from storeapp import models
from django.shortcuts import render, get_object_or_404
from storeapp.forms import UserRegisterForm,UserInfoForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.


class Indexview(TemplateView):
    template_name = 'storeapp/index.html'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        categories = models.Categories.objects.all()
        items = models.Item.objects.filter(available=True)[:9]
        context['items'] = items
        context['categories'] = categories
        return context

def item_detail(request,slug):
    item = models.Item.objects.filter(slug=slug)
    return render(request,'storeapp/item_detail.html',{'item':item})


def cat_query(request,cat_slug):
    category = models.Categories.objects.all()
    cat = get_object_or_404(models.Categories,slug=cat_slug)
    brand = models.Brand.objects.filter(category=cat)
    catn = cat.cat_name
    items = models.Item.objects.filter(brand__category__cat_name=catn)
    return render(request,'storeapp/item_query.html',{'items':items,'brand':brand,'category':category})

def brand_query(request,brand_slug):
    category = models.Categories.objects.all()
    brands = get_object_or_404(models.Brand,slug=brand_slug)
    catn = brands.category
    items = models.Item.objects.filter(brand=brands)
    brand = models.Brand.objects.filter(category__cat_name=catn)
    return render(request,'storeapp/item_query.html',{'items':items,'brand':brand,'category':category})


@login_required
def con_order(request):
    cart = Cart(request)
    return render(request,"storeapp/order.html",{"cart":cart})

@login_required
def fin_order(request):
    user1 = request.user
    use = models.UserInfo.objects.get(user=user1)
    cart = Cart(request)
    for item in cart:
        models.Order.objects.create(user=use,product=item['product'],
                                    price=item['price'],quantity=item['quantity'])
    cart.clear()
    return render(request,"storeapp/order_success.html",{'use':use})


def searchview(request):
    if request.method == 'GET':
        obj = request.GET.get('search')
        if obj:
            try:
                search_item = models.Item.objects.filter(item_name__icontains=obj)
            except ExplicitException:
                pass
            # search_item = models.Item.objects.filter(brand__category__cat_name__icontains=obj)
            return render(request,"storeapp/item_search.html",{'search_item':search_item,'obj':obj})
    else:
        return render(request,"storeapp/item_search.html",{'obj':obj})


def loginview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('storeapp:index'))
            else:
                return HttpResponse('User is not active')
        else:
            return HttpResponse('wrong username and password')
    else:
        return render(request,'storeapp/base.html',{})

def signupview(request):
    if request.method == "POST":
        user_form = UserRegisterForm(request.POST)
        info_form = UserInfoForm(request.POST)

        if user_form.is_valid() and info_form.is_valid():
            new = user_form.save(commit=False)
            new.set_password(user_form.cleaned_data['password'])  #does encryption
            new.save()
            info = info_form.save(commit=False)
            info.user = new
            info.save()
            return render(request,'storeapp/signup.html',{'user_form':user_form,'info_form':info_form})
        else:
            return HttpResponse('ValidationError')
    else:
        user_form = UserRegisterForm()
        info_form = UserInfoForm()
        return render(request,'storeapp/signup.html',{'user_form':user_form,'info_form':info_form})
