from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.core.paginator import Paginator, InvalidPage
from django.http import HttpResponse, Http404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django import forms
from .models import *
from .forms import *
from basket.models import Cart
from basket.forms import CartItemCount
from django.shortcuts import render
from django.contrib.auth.decorators import login_required






class Navbar(TemplateView):
	template_name = 'includes/navbar.html'
	def get_context_data(self, **kwargs):
		context = super(Navbar, self).get_context_data(**kwargs)
		context['login_img'] = Photo.objects.get(name='login').photo
		return context









class CategoryListMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CategoryListMixin, self).get_context_data(**kwargs)
		context['cats'] = Category.objects.order_by('name')
		context['default_img'] = Photo.objects.get(name="Default").photo
		return context




class GoodListView(ListView, CategoryListMixin):
	"""
	Класс удобный для вывода СПИСКА чего либа 
	"""

	template_name = 'main_page/list_goods.html'
	paginate_by = 1
	cat = None
	form = None
	cart = None
	opt_user = None
	def get(self, request, *args, **kwargs):
		"""
		Присваивает gеременной контекста данных
		в которой должен храниться список
		записей, этот самый список.
		(То есть инициализирует сам context)
		"""

		if request.user.is_authenticated():
			try:
				self.opt_user = request.user.customer_set.first().opt
			except:
				pass

		self.form = CartItemCount
		if self.kwargs['cat_id']:
			self.cat = Category.objects.get(pk=kwargs['cat_id'])
		# request.session['basket_goods'] = {}
		try:
			cart_id = request.session['cart_id']
			self.cart = Cart.objects.get(id=cart_id)
		except:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		print(self.cart.id, 'cart_id')
		return super(GoodListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		"""
		Создает контекст данных
		"""

		# Формирует сам контекст данных и заполнит его начальными данными, 
		# в частности значениями полученными контроллером параметров.

		context = super(GoodListView, self).get_context_data(**kwargs) 
		context['categorymy'] = self.cat
		context['login_img'] = Photo.objects.get(name='login')
		context['logout_img'] = Photo.objects.get(name='logout')
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context

	def get_queryset(self): 
		"""
		Этот метод вызврощает спичсок 
		записей которые будут выводиться 
		на экран 
		""" 

		if self.cat:
			return Goods.objects.filter(category=self.cat).order_by('code')
		else:
			return Goods.objects.all().order_by('code')


	def post(self, request, *args, **kwargs):
		if self.form.is_valid():
			self.form.save()
		else:
			return super(GoodListView, self).post(request, *args, **kwargs)




class GoodDetailView(DetailView, CategoryListMixin):
	"""Ищет объект по pk
	если его нет то ищет по pk_url_kwargs
	"""
	template_name =  'main_page/good_page.html'
	model = Goods
	context_object_name = 'good'
	# pk_url_kwargs = 'code'

	
	def get_context_data(self, **kwargs):
		"""Вот решение: вы можете создать подкласс от DetailView 
		и переопределить в нем метод get_context_data. 
		Реализация метода по умолчанию просто добавляет объект, 
		который будет доступен в шаблоне. Но переопределив метод, 
		вы можете добавить любые дополнительные данные(расширить контекст):
		"""

		context = super(GoodDetailView, self).get_context_data(**kwargs)
		try:
			context['pn'] = self.request.GET['page']
		except KeyError:
			context['pn'] = 1
		context['cats'] = Category.objects.order_by('name')
		return context


	def get_object(self):
		"""Возвращает единственный объект, отображаемый этим представлением. 
		Если queryset предусмотрено, этот запрос будет использоваться как источник объектов; 
		в противном случае get_queryset(). get_object()ищет pk_url_kwargаргумент в аргументах представления; 
		если этот аргумент найден, этот метод выполняет поиск на основе первичного ключа с использованием этого значения. 
		Если этот аргумент не найден, он ищет slug_url_kwargаргумент и выполняет поиск в slug с помощью slug_field.
		"""

		return Goods.objects.get(code=self.kwargs['code'])















# Классы форм:





class GoodEditMixin(CategoryListMixin):

	def get_context_data(self, **kwargs):
		context = super(GoodEditMixin, self).get_context_data(**kwargs)
		try:
			context['pn'] = self.request.GET['page']
		except KeyError:
			context['pn'] = 1
		return context


class GoodEditView(ProcessFormView):
	def post(self, request, *args, **kwargs):
		try:
			pn = request.GET['page']
		except KeyError:
			pn = 1
		# Адресс на который будет выполнено перенаправление после успешного добавления ил правки записи
		self.success_url = "{}?page={}".format(self.success_url, pn)
		return super(GoodEditView, self).post(request, *args, **kwargs) 




class GoodCreate(SuccessMessageMixin, CreateView, GoodEditMixin):
	#form_class = GoodForm
	form_class = GoodForm
	template_name = 'main_page/good_add.html'
	# def get(self, request, *args, **kwargs):
	# 	if self.kwargs['cat_id'] != None:
	# 		self.initial['category'] = Category.objects.get(pk = self.kwargs['cat_id'])
	# 	return super(GoodCreate, self).get(request, *args,**kwargs)

	def post(self, request, *args, **kwargs):
		"""
		reverse формирует интернет адрес принимает имя, 
		указанного параметра name функции url  в привязке интернет адреса
		"""
		if self.kwargs['cat_id'] == None:
			cat = Category.objects.first()
		else:
			cat = Category.objects.get(pk=self.kwargs['cat_id'])
		self.form = GoodForm(request.POST)
		if self.form.is_valid():
			self.form.save()
			messages.add_message(request, messages.SUCCESS, "Товар создан")
			return redirect('index')
		else:
			return super(GoodCreate, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		"""
		Формирует в контексте данных переменную форм
		"""
		context = super(GoodCreate, self).get_context_data(**kwargs)
		context['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
		return context










class GoodUpdate(UpdateView, GoodEditMixin, GoodEditView):
	model = Goods
	template_name = 'main_page/good_edit.html'
	# pk_url_kwarg = 'code'
	fields = ['code', 'articul', 'description', 'price']

	def post(self, request, *args, **kwargs):
		self.success_url = reverse('index',  kwargs={'cat_id': Goods.objects.get(code=kwargs['code']).category.id})
		return super(GoodUpdate, self).post(request, *args, ** kwargs)

	def get_object(self):
		return Goods.objects.get(code=self.kwargs['code'])







class GoodDelete(DeleteView, GoodEditMixin, GoodEditView):
	model = Goods
	template_name = 'main_page/good_delete.html'
	pk_url_kwarg = 'code'

	def post(self, request, *args, **kwargs):
		#self.success_url = reverse('index',  kwargs={'cat_id': Goods.objects.get(pk=kwargs['code']).category.id})
		self.success_url = reverse_lazy('index')
		return super(GoodDelete, self).post(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(GoodDelete, self).get_context_data(**kwargs)
		context['good'] = Goods.objects.get(pk=self.kwargs['code'])
		return context





class AddFiles(SuccessMessageMixin, TemplateView):
	template_name = 'main_page/add_files.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = UploadFiles(initial = {'name': 'blabla'})
		return super(AddFiles, self).get(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		"""
		reverse формирует интернет адрес принимает имя, 
		указанного параметра name функции url  в привязке интернет адреса
		"""

		self.form = UploadFiles(request.POST, request.FILES)
		if self.form.is_valid():
			self.form.save()
			messages.add_message(request, messages.SUCCESS, "Товар создан")
			return redirect('index')
		else:
			return super(AddFiles, self).post(request, *args, **kwargs)



	def get_context_data(self, **kwargs):
		context = super(AddFiles, self).get_context_data(**kwargs)
		context['form'] = self.form
		return context





def uploads_photo(request, id=None):
	form = UploadImg(request.POST or None, request.FILES or None)
	if form.is_valid():
		# print(request.POST)
		post = form.save(commit=False)
		post.save()
		return redirect('index')
	else:
		form = UploadImg()
	return render(request, 'main_page/add_files.html', {'form': form})











# def my_profile(request):
# 	my_user_profile = Profile.objects.filter(user=request.user).first()
# 	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
# 	context = {
# 		'my_orders': my_orders
# 	}

# 	return render(request, 'main_page/profile.html', context)






# def get_user_pending_order(request):
#     # get order for the correct user
#     user_profile = get_object_or_404(Profile, user=request.user)
#     order = Order.objects.filter(owner=user_profile, is_ordered=False)
#     if order.exists():
#         # get the only order in the list of filtered orders
#         return order[0]
#     return 0


# @login_required()
# def add_to_cart(request, **kwargs):
#     # get the user profile
#     user_profile = get_object_or_404(Profile, user=request.user)
#     # filter products by id
#     product = Product.objects.filter(id=kwargs.get('item_id', "")).first()
#     # check if the user already owns this product
#     if product in request.user.profile.ebooks.all():
#         messages.info(request, 'You already own this ebook')
#         return redirect(reverse('products:product-list')) 
#     # create orderItem of the selected product
#     order_item, status = OrderItem.objects.get_or_create(product=product)
#     # create order associated with the user
#     user_order, status = Order.objects.get_or_create(owner=user_profile, is_ordered=False)
#     user_order.items.add(order_item)
#     if status:
#         # generate a reference code
#         user_order.ref_code = generate_order_id()
#         user_order.save()

#     # show confirmation message and redirect back to the same page
#     messages.info(request, "item added to cart")
#     return redirect(reverse('products:product-list'))


# @login_required()
# def delete_from_cart(request, item_id):
#     item_to_delete = OrderItem.objects.filter(pk=item_id)
#     if item_to_delete.exists():
#         item_to_delete[0].delete()
#         messages.info(request, "Item has been deleted")
#     return redirect(reverse('shopping_cart:order_summary'))


# @login_required()
# def order_details(request, **kwargs):
#     existing_order = get_user_pending_order(request)
#     context = {
#         'order': existing_order
#     }
#     return render(request, 'shopping_cart/order_summary.html', context)


# @login_required()
# def checkout(request):
#     existing_order = get_user_pending_order(request)
#     publishKey = settings.STRIPE_PUBLISHABLE_KEY
#     if request.method == 'POST':
#         try:
#             token = request.POST['stripeToken']

#             charge = stripe.Charge.create(
#                 amount=100*existing_order.get_cart_total(),
#                 currency='usd',
#                 description='Example charge',
#                 source=token,
#             )
#             return redirect(reverse('shopping_cart:update_records',
#                         kwargs={
#                             'token': token
#                         })
#                     )

#         except stripe.CardError as e:
#             message.info(request, "Your card has been declined.")
            
#     context = {
#         'order': existing_order,
#         'STRIPE_PUBLISHABLE_KEY': publishKey
#     }

#     return render(request, 'shopping_cart/checkout.html', context)


# @login_required()
# def update_transaction_records(request, token):
#     # get the order being processed
#     order_to_purchase = get_user_pending_order(request)

#     # update the placed order
#     order_to_purchase.is_ordered=True
#     order_to_purchase.date_ordered=datetime.datetime.now()
#     order_to_purchase.save()
    
#     # get all items in the order - generates a queryset
#     order_items = order_to_purchase.items.all()

#     # update order items
#     order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())

#     # Add products to user profile
#     user_profile = get_object_or_404(Profile, user=request.user)
#     # get the products from the items
#     order_products = [item.product for item in order_items]
#     user_profile.ebooks.add(*order_products)
#     user_profile.save()

    
#     # create a transaction
#     transaction = Transaction(profile=request.user.profile,
#                             token=token,
#                             order_id=order_to_purchase.id,
#                             amount=order_to_purchase.get_cart_total(),
#                             success=True)
#     # save the transcation (otherwise doesn't exist)
#     transaction.save()


#     # send an email to the customer
#     # look at tutorial on how to send emails with sendgrid
#     messages.info(request, "Thank you! Your purchase was successful!")
#     return redirect(reverse('accounts:my_profile'))


# def success(request, **kwargs):
#     # a view signifying the transcation was successful
#     return render(request, 'shopping_cart/purchase_success.html', {})
