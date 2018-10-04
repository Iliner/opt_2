import decimal
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Cart, CartItem
from .forms import CartItemCount, CartItemFormset
from main_page.models import Goods, Photo
from django.views.decorators.csrf import csrf_exempt

import smtplib
from email.mime.text import MIMEText
from email.header import Header



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
	opt_user = None

	def get(self, request, *args, **kwargs):
		self.form = CartItemCount
		self.cart = cart_init(request)
		self.opt_user = request.user.customer_set.first().opt
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
		context['opt_user'] = self.opt_user
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
	user = request.user
	customer = request.user.customer_set.first()
	have_cart = customer.baskets.all().filter(paid_for=False).exists()
	if have_cart:
		cart = customer.baskets.all().filter(paid_for=False).first()
		request.session['cart_id'] = cart.id
	else:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		customer.baskets.add(cart)
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	
	# try:
	# 	cart_id = request.session['cart_id']
	# 	cart = Cart.objects.get(id=cart_id)
	# except:
	# 	cart = Cart()
	# 	cart.save()
	# 	cart_id = cart.id
	# 	customer.baskets.add(cart)
	# 	request.session['cart_id'] = cart_id
	# 	cart = Cart.objects.get(id=cart_id)
	return cart


def opt_price(good, opt):
	price = None
	opt = str(opt)
	if opt == '1':
		price = good.price
	elif opt == '2':
		price = good.price_2
	elif opt == '3':
		price = good.price_3
	elif opt == '5':
		price = good.price_5
	elif opt == '6':
		price = good.price_6
	return price


def add_view(request):
	"""Контролер для корзины

	Добовляет позицию в корзину
	"""

	opt_user = request.user.customer_set.first().opt
	cart = cart_init(request)
	if request.method == 'POST':
		product = Goods.objects.get(code=request.POST['code'])
		if int(request.POST['count']) > 0:
			price = opt_price(product, opt_user)
			if cart.items.all().exists():
				for item in cart.items.all():
					if str(item.product.code) == str(request.POST['code']):
						exists = 1
						item = item
						break
					else:
						exists = 0
				if exists:	
					print("есть")
					item.count = request.POST['count']
					item.item_total = decimal.Decimal(request.POST['count']) * decimal.Decimal(price)
					item.save()
				else:
					print("нет")
					need_item = CartItem()
					need_item.product = product
					need_item.count = request.POST['count']
					need_item.item_total = decimal.Decimal(request.POST['count']) * decimal.Decimal(price)
					need_item.price = price
					print('need_item.price', need_item.price)
					need_item.customer = request.user.customer_set.first()  
					need_item.save()
					cart.items.add(need_item)
					print(cart.id, 'cart id exists')
			else:	
				need_item = CartItem()
				need_item.product = product
				need_item.count = request.POST['count']
				need_item.item_total = decimal.Decimal(request.POST['count']) * decimal.Decimal(price)
				need_item.price = price
				print('need_item.price ', need_item.price)
				need_item.customer = request.user.customer_set.first()  
				need_item.save()
				cart.items.add(need_item)
				print(cart.id, 'cart id exists')
				cart.save()

		elif int(request.POST['count']) == 0:
			price = opt_price(product, opt_user)
			if cart.items.all().filter(product__code=request.POST['code']).exists():
				cart.items.all().filter(product__code=request.POST['code']).delete()
				cart.save()


	cart.cart_total = cart.cart_total_summ()
	cart.save()
	return HttpResponse(cart.cart_total)



	# if request.method == 'POST':
	# 	product = Goods.objects.get(code=request.POST['code'])
	# 	if int(request.POST['count']) > 0:
	# 		if CartItem.objects.filter(product__code=request.POST['code']).exists():
	# 			need_item = CartItem.objects.get(product__code=request.POST['code'])
	# 			need_item.count = request.POST['count']
	# 			need_item.item_total = int(request.POST['count']) * int(need_item.product.price)
				
	# 			need_item.save()
	# 			cart.items.add(need_item)
	# 			print(cart.id, 'cart id exists')
	# 			cart.save()
	# 		else:			
	# 			# print('not exists')
	# 			# print(request.POST['count'], request.POST['code'], 'here')
	# 			print(cart.id, 'cart id exists no')
	# 			cart_item = CartItem
	# 			new_cart_object = cart_item.objects.create(product=product, count=request.POST['count'], item_total=product.price * int(request.POST['count']))
	# 			cart.items.add(new_cart_object)
	# 			cart.save()
	# 	elif int(request.POST['count']) == 0:
	# 		need_item = CartItem.objects.get(product__code=request.POST['code']).delete()
				

	# cart.cart_total = cart.cart_total_summ()
	# cart.save()
	# return HttpResponse(cart.cart_total)
	#return HttpResponse(2)

                                                                                                                            









def smtp_send(
	smtp_host, smtp_port, 
	smtp_login, smtp_password, 
	send_to, message_text, 
	header_text):
	msg = MIMEText(message_text, 'plain', 'utf-8')
	msg['Subject'] = Header(header_text, 'utf-8')
	msg['From'] = smtp_login
	msg["To"] = send_to
	smtpObj = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)
	smtpObj.login(smtp_login, smtp_password)
	smtpObj.sendmail(smtp_login, send_to, msg.as_string())
	smtpObj.quit()





@csrf_exempt
def confirm_order(request):
	cart = cart_init(request)
	cart.paid_for = True
	cart_id = cart.id
	cart.save()
	paid_for = 'True'

	user = request.user
	user_email = user.email
	user_customer = user.customer_set.first()

	smtp_host = "smtp.mail.ru"
	smtp_port = "465"
	smtp_login = "stock@kvam.ru"
	smtp_password = "AT3TeC&5lshf"
	body_text = ""

	


	for item in cart.items.all():
		body_text = "{}\n Артикул: {} Цена: {}".format(
			body_text, 
			item.product.articul, 
			item.product.price)

	header_text_to_customer = "opt-online.ru Ваш заказ №{}".format(cart_id)
	header_text_to_admin = "Заказчик {} {} Стоймость {}".format(
		user.first_name, 
		user.last_name, 
		cart.cart_total)
	
	send_to = str(user_email)
	send_to_admin = 'mynamekasatkin@gmail.com'
	message_text = body_text
	smtp_send(
		smtp_host, smtp_port, 
		smtp_login, smtp_password, 
		send_to_admin, message_text, 
		header_text_to_admin)
	smtp_send(
		smtp_host, smtp_port, 
		smtp_login, smtp_password, 
		send_to, message_text, 
		header_text_to_customer)
	reverse_lazy('index')
	return HttpResponse(paid_for)












class HistoryOrderView(ListView, CartCommonMixin):
	template_name = 'basket/history_order.html'
	paginate_by = 100
	customer = None

	def get(self, request, *args, **kwargs):
		self.customer = request.user.customer_set.first()
		for cart in self.customer.baskets.all().filter(paid_for=True).order_by('-date'):
			for item in cart.items.all():
				print(item.product.code)
		return super(HistoryOrderView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HistoryOrderView, self).get_context_data(**kwargs) 
		return context

	def get_queryset(self): 
		carts_order = self.customer.baskets.all().filter(paid_for=True).order_by('-date')
		return carts_order




@csrf_exempt
def delete_item(request):
	cart = cart_init(request)
	if request.method == 'POST':
		if cart.items.all().filter(product__code=request.POST['code']).exists():
			cart.cart_total = cart.cart_total - cart.items.all().filter(product__code=request.POST['code']).first().item_total
			cart.items.all().filter(product__code=request.POST['code']).delete()
			cart.save()
	CartView()		
	return HttpResponse(cart.cart_total)