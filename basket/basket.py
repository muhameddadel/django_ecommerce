from decimal import Decimal

from django.conf import settings

from checkout.models import DeliveryOptions
from store.models import Product


class Basket():
    """
    A base Basket class providing some default behaviors that
    can be inherited or overrided, as necessary.
    """
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.regular_price), 'qty': qty}

        self.save()

    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products
        """
        product_ids = self.basket.keys()
        prodcuts = Product.objects.filter(id__in = product_ids)
        basket = self.basket.copy()

        for product in prodcuts:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
            
    def __len__(self):
        """
        Get the basket data and count the the quntity of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def update(self, product, qty):
        """
        Updata values in session data
        """
        product_id = str(product)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        
        self.save()

    def get_subtotal_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

    def get_delivery_price(self):
        newprice = 0.00
        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        return newprice

    def get_total_price(self):
        newprice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "purchase" in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session["purchase"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newprice)
        return total
    
    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def delete(self, product):
        """
        Delete item from session data
        """
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()
            
    def save(self):
        self.session.modified = True

    def clear(self):
        """
        Remove basket from session
        """
        del self.session[settings.BASKET_SESSION_ID]
        self.save()