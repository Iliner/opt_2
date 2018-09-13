import decimal
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from .models import Cart, CartItem
from main_page.models import Goods


def cart_view(request):
	cart = Cart.objects.first()
	context = {
		'cart': cart
	}
	return render(request, 'basket/cart.html', context)



def add_to_card_view(request, code):
	product = Goods.objects.get(code=code)
	new_item, _ = CartItem.objects.get_or_create(
		product=product, 
		count=1, 
		item_total=product.price
		)
	cart = Cart.objects.first()
	cart.items.add(new_item)
	cart.cart_total += decimal.Decimal(product.price)
	cart.save()
	return HttpResponseRedirect('/cart/')

