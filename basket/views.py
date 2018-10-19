import decimal
import csv

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import Cart, CartItem, Manager
from .forms import CartItemCount, CartItemFormset
from main_page.models import Goods, Photo

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
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
	manager = None
	customer = None

	def get(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)

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




class MenegerView(TemplateView):
	template_name = 'main_page/footer_manager_data.html'


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
	elif opt == '7':
		price = good.price_7
	elif opt == '8':
		price = good.price_8
	elif opt == '9':
		price = good.price_9
	elif opt == '10':
		price = good.price_10
	elif opt == '11':
		price = good.price_11
	elif opt == '12':
		price = good.price_12
	elif opt == '13':
		price = good.price_13
	elif opt == '14':
		price = good.price_14
	elif opt == '15':
		price = good.price_15
	elif opt == '6':
		price = good.price_6
	elif opt == '17':
		price = good.price_17
	elif opt == '18':
		price = good.price_18
	elif opt == '19':
		price = good.price_19
	elif opt == '20':
		price = good.price_20
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
			request.session['goods_card'][request.POST['code']] = int(request.POST['count'])
			print('goods_card', request.session['goods_card'])
			print('url', request.get_full_path())
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
			request.session['goods_card'].pop(request.POST['code'])

			price = opt_price(product, opt_user)
			if cart.items.all().filter(product__code=request.POST['code']).exists():
				cart.items.all().filter(product__code=request.POST['code']).delete()
				cart.save()


	cart.cart_total = cart.cart_total_summ()
	cart.save()
	return HttpResponse(cart.cart_total)



                                                                                                                          





def smtp_send(
	smtp_host, smtp_port, 
	smtp_login, smtp_password, 
	send_to, message_text, 
	header_text, admin=None, attachment=None):
	# if admin:
	
	# else:
	print('h', smtp_login, smtp_password)
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
	send_mail_us(request)
	send_mail_customer(request)
	paid_for = 'True'
	reverse_lazy('index')
	return HttpResponse(paid_for)






def mail_data(request):
	cart = cart_init(request)
	cart.paid_for = True
	cart_id = cart.id
	cart.save()



def send_mail_us(request):
	cart = cart_init(request)
	cart.paid_for = True
	cart_id = cart.id
	cart.save()
	paid_for = 'True'
	user = request.user
	path_csv = "uploads/basket/csv_to_send/{}_{}_{}.csv".format(user.first_name, user.last_name, cart_id)
	name_csv = "{}_{}_{}.csv".format(user.first_name, user.last_name, cart_id)
	with open(path_csv, 'w', newline='') as csvfile:
	    spamwriter = csv.writer(
	    	csvfile, 
	    	delimiter=';',
          	quotechar='|', 
          	quoting=csv.QUOTE_MINIMAL
          	)

	    for item in cart.items.all():	
	    	spamwriter.writerow([item.product.code, item.count])


	email_admin = User.objects.get(username='ivan').email
	emailto = email_admin
	fileToSend = path_csv
	smtp_login = "stock@kvam.ru"
	username = smtp_login
	password = "AT3TeC&5lshf"
	header_text_to_admin = "Заказчик {} {} Стоймость {}".format(
		user.first_name, 
		user.last_name, 
		cart.cart_total)

	msg = MIMEMultipart()
	msg["From"] = smtp_login
	msg["To"] = emailto
	msg["Subject"] = header_text_to_admin
	msg.preamble = "help I cannot send an attachment to save my life"

	ctype, encoding = mimetypes.guess_type(fileToSend)
	if ctype is None or encoding is not None:
	    ctype = "application/octet-stream"

	maintype, subtype = ctype.split("/", 1)

	if maintype == "text":
	    fp = open(fileToSend)
	    attachment = MIMEText(fp.read(), _subtype=subtype)
	    fp.close()
	elif maintype == "image":
	    fp = open(fileToSend, "rb")
	    attachment = MIMEImage(fp.read(), _subtype=subtype)
	    fp.close()
	elif maintype == "audio":
	    fp = open(fileToSend, "rb")
	    attachment = MIMEAudio(fp.read(), _subtype=subtype)
	    fp.close()
	else:
	    fp = open(fileToSend, "rb")
	    attachment = MIMEBase(maintype, subtype)
	    attachment.set_payload(fp.read())
	    fp.close()
	    encoders.encode_base64(attachment)

	attachment.add_header("Content-Disposition", "attachment", filename=name_csv)
	msg.attach(attachment)
	server = smtplib.SMTP('smtp.mail.ru:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(smtp_login, emailto, msg.as_string())
	server.quit()




def send_mail_customer(request):
	cart = cart_init(request)
	cart.paid_for = True
	cart_id = cart.id
	cart.save()
	paid_for = 'True'

	user = request.user
	user_email = str(user.email)
	user_email_brand = user_email.split('@')[-1]
	user_customer = user.customer_set.first()

	smtp_login = "stock@kvam.ru"
	smtp_password = "AT3TeC&5lshf"
	smtp_port = "465"
	smtp_host = "smtp.mail.ru"
	body_text = ""

	
	for item in cart.items.all():
		print('item.product.articul', item.product.articul)
		body_text = "{}\n Артикул: {} Цена: {} Кол-во: {}".format(
			body_text, 
			item.product.articul, 
			item.product.price,
			item.count,
			)

	header_text_to_customer = "opt-online.ru Ваш заказ №{}".format(cart_id)
	send_to = str(user_email)
	message_text = body_text
	smtp_send(
		smtp_host, smtp_port, 
		smtp_login, smtp_password, 
		send_to, message_text, 
		header_text_to_customer)




class HistoryOrderView(ListView, CartCommonMixin):
	template_name = 'basket/history_order.html'
	paginate_by = 100
	customer = None
	manager = None
	
	def get(self, request, *args, **kwargs):
		self.customer = request.user.customer_set.first()
		for cart in self.customer.baskets.all().filter(paid_for=True).order_by('-date'):
			for item in cart.items.all():
				print(item.product.code)
		try:
			self.manager = Manager.objects.get(customers=self.customer)
		except Exception as err:
			print(err)	

		return super(HistoryOrderView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(HistoryOrderView, self).get_context_data(**kwargs) 
		if self.manager:
			context['manager_first_name'] = self.manager.first_name
			context['manager_last_name'] = self.manager.last_name
			context['manager_mail_work'] = self.manager.mail_work
			context['manager_phone_number_work'] = self.manager.phone_number_work
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