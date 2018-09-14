import decimal
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Cart, CartItem
from .forms import Order
from main_page.models import Goods, Photo



class CartCommonMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CartCommonMixin, self).get_context_data(**kwargs)
		context['default_img'] = Photo.objects.get(name="Default").photo
		return context



class CartView(TemplateView, CartCommonMixin):
	template_name = 'basket/cart.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = Order
		return super(CartView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CartView, self).get_context_data(**kwargs)
		context['form'] = self.form
		context['cart'] = Cart.objects.first()
		return context

	def post(self, request, *args, **kwargs):
		if self.form.is_valid():
			self.form.save()
		else:
			return super(CartView, self).post(request, *args, **kwargs)










class DeletePosition(DeleteView):
	model = CartItem
	template_name = 'basket/cart.html'
	pk_url_kwarg = 'pk'

	def get_context_data(self, **kwargs):
		context = super(DeletePosition, self).get_context_data(**kwargs)
		context['good'] = CartItem.objects.get(pk=self.kwargs['pk'])
		return context

	def post(self, request, *args, **kwargs):
		self.success_url = reverse_lazy('index')
		return super(DeletePosition, self).post(request, *args, **kwargs)













# def cart_view(request):
# 	cart = Cart.objects.first()
# 	context = {
# 		'cart': cart,
# 		'default_img': Photo.objects.get(name="Default").photo
# 	}
# 	return render(request, 'basket/cart.html', context)



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

