from decimal import Decimal
from django.conf import settings
from storeapp.models import Item


class Cart(object):
    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self,item,quantity=1,update_quantity=False):
        """
        Add or update quantity method
        """
        id = item.pk
        if id not in self.cart:
            self.cart[id] = { 'quantity': 0,
                              'price':str(item.price)
                                   }
        if update_quantity:
            self.cart[id]['quantity'] = quantity
        else:
            self.cart[id]['quantity'] +=quantity
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self,id):
        # id = item.pk
        if id in self.cart:
            del self.cart[id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from
        the database
        """
        product_ids = self.cart.keys()
         # get the product objects and add them to the cart
        products = Item.objects.filter(id__in=product_ids)
        for product in products:
             self.cart[str(product.id)]['product'] = product

        for items in self.cart.values():
            items['price'] = Decimal(items['price'])
            items['total_price'] = items['price']*items['quantity']
            yield items

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(items['quantity'] for items in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity']for item in self.cart.values())

    def clear(self):
         # remove cart from session
         del self.session[settings.CART_SESSION_ID]
         self.session.modified = True
