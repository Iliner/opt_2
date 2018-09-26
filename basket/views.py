import decimal
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Cart, CartItem
from .forms import CartItemCount, CartItemFormset
from main_page.models import Goods, Photo







class CartCommonMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CartCommonMixin, self).get_context_data(**kwargs)
		context['default_img'] = Photo.objects.get(name="Default").photo
		return context



class CartView(TemplateView, CartCommonMixin):
	template_name = 'basket/cart.html'
	form = None
	cart_id = None
	cart = None

	def get(self, request, *args, **kwargs):
		self.form = CartItemCount
		self.cart = cart_init(request)
		return super(CartView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(CartView, self).get_context_data(**kwargs)
		cart_items = CartItem.objects.all()
		dict_count = {}
		for items in cart_items.all():
			dict_count[items.product.code] = items.count
		#print(dict_count)
		context['dict_count'] = dict_count
		context['form'] = self.form
		context['cart'] = self.cart
		# context['cart_id'] = self.cart_id
		return context

	def post(self, request, *args, **kwargs):
		if self.form.is_valid():
			self.form.save()
		else:
			return super(CartView, self).post(request, *args, **kwargs)












# class CartView(TemplateView, CartCommonMixin):
# 	template_name = 'basket/cart.html'
# 	formset = None
# 	cart_id = None

# 	def get(self, request, *args, **kwargs):
# 		self.formset = CartItemFormset()
# 		try:
# 			cart_id = request.session['cart_id']
# 			cart = Cart.objects.get(id=cart_id)
# 			#request.session['total'] = cart.cart_total
# 		except:
# 			cart = Cart()
# 			cart.save()
# 			self.cart_id = cart.id
# 			request.session['cart_id'] = self.cart_id
# 		return super(CartView, self).get(request, *args, **kwargs)

# 	def get_context_data(self, **kwargs):
# 		context = super(CartView, self).get_context_data(**kwargs)
# 		cart_items = CartItem.objects.all()
# 		dict_count = {}
# 		for items in cart_items.all():
# 			dict_count[items.product.code] = items.count
# 		#print(dict_count)
# 		context['dict_count'] = dict_count
# 		context['formset'] = self.formset
# 		context['cart'] = Cart.objects.first()
# 		context['cart_id'] = self.cart_id
# 		return context

# 	def post(self, request, *args, **kwargs):
# 		if self.formset.is_valid():
# 			self.formset.save()
# 		else:
# 			return super(CartView, self).post(request, *args, **kwargs)




























class DeletePosition(DeleteView):
	model = CartItem
	template_name = 'basket/cart.html'
	pk_url_kwarg = 'pk'
	print('4')

	def get(self, *args, **kwargs):
		cart = cart_init(request)
		cart.cart_total = cart.cart_total - CartItem.objects.get(pk=self.kwargs['pk']).product.price 
		return super(DeletePosition, self).get(*args)

	def get_context_data(self, **kwargs):
		context = super(DeletePosition, self).get_context_data(**kwargs)
		cart = Cart.objects.first()
		cart.cart_total = cart.cart_total - int(CartItem.objects.get(pk=self.kwargs['pk']).product.price) 
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



def delete_from_cart_view(request, code):
	pass



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




def cart_init(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	return cart



def add_view(request):
	"""Контролер для корзины

	Добовляет позицию в корзину
	"""
	#cart = Cart.objects.first()

	cart = cart_init(request)
	print(cart.id, 'cart asdadsa')
	if request.method == 'POST':
		product = Goods.objects.get(code=request.POST['code'])
		if int(request.POST['count']) > 0:
			if CartItem.objects.filter(product__code=request.POST['code']).exists():
				need_item = CartItem.objects.get(product__code=request.POST['code'])
				need_item.count = request.POST['count']
				need_item.item_total = int(request.POST['count']) * int(need_item.product.price)
				
				need_item.save()
				cart.items.add(need_item)
				print(cart.id, 'cart id exists')
				cart.save()
			else:			
				# print('not exists')
				# print(request.POST['count'], request.POST['code'], 'here')
				print(cart.id, 'cart id exists no')
				cart_item = CartItem
				new_cart_object = cart_item.objects.create(product=product, count=request.POST['count'], item_total=product.price * int(request.POST['count']))
				cart.items.add(new_cart_object)
				cart.save()
		elif int(request.POST['count']) == 0:
			need_item = CartItem.objects.get(product__code=request.POST['code']).delete()
				

	cart.cart_total = cart.cart_total_summ()
	cart.save()
	return HttpResponse(cart.cart_total)

                                                                                                                            

























