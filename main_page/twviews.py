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


	def get(self, request, *args, **kwargs):
		"""
		Присваивает gеременной контекста данных
		в которой должен храниться список
		записей, этот самый список.
		(То есть инициализирует сам context)
		"""

		if self.kwargs['cat_id']:
			self.cat = Category.objects.get(pk=kwargs['cat_id'])


		return super(GoodListView, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		"""
		Создает контекст данных
		"""

		# Формирует сам контекст данных и заполнит его начальными данными, 
		# в частности значениями полученными контроллером параметров.
		context = super(GoodListView, self).get_context_data(**kwargs) 
		context['categorymy'] = self.cat

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




# class GoodCreate(CreateView, GoodEditMixin):
# 	#form_class = GoodForm
# 	model = Goods
# 	template_name = 'main_page/good_add.html'
# 	fields = ['code', 'articul', 'producer', 'category', 'description', 'price']

# 	def get(self, request, *args, **kwargs):
# 		if self.kwargs['cat_id'] != None:
# 			self.initial['category'] = Category.objects.get(pk = self.kwargs['cat_id'])
# 		return super(GoodCreate, self).get(request, *args,**kwargs)

# 	def post(self, request, *args, **kwargs):
# 		"""
# 		reverse формирует интернет адрес принимает имя, 
# 		указанного параметра name функции url  в привязке интернет адреса
# 		"""
# 		self.success_url = reverse('good_page', kwargs={'code': 8922})
# 		return super(GoodCreate, self).post(request, *args, **kwargs)

# 	def get_context_data(self, **kwargs):
# 		"""
# 		Формирует в контексте данных переменную форм
# 		"""
# 		context = super(GoodCreate, self).get_context_data(**kwargs)
# 		context['category'] = Category.objects.get(pk=self.kwargs['cat_id'])
# 		return context



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




	# def get_object(self):
	# 	"""Возвращает единственный объект, отображаемый этим представлением. 
	# 	Если queryset предусмотрено, этот запрос будет использоваться как источник объектов; 
	# 	в противном случае get_queryset(). get_object()ищет pk_url_kwargаргумент в аргументах представления; 
	# 	если этот аргумент найден, этот метод выполняет поиск на основе первичного ключа с использованием этого значения. 
	# 	Если этот аргумент не найден, он ищет slug_url_kwargаргумент и выполняет поиск в slug с помощью slug_field.
	# 	"""

	# 	return Goods.objects.get(code=self.kwargs['code'])

# class AddFiles(TemplateView):
# 	template_name = 'main_page/add_files.html'
# 	form = UploadFiles


# 	def post(self, request, *args, **kwargs):
# 		self.form = UploadFiles(request.POST, request.FILES)
# 		if self.form.is_valid():
# 			self.form.save()
# 			return redirect('index')
# 		else:
# 			return super(GoodCreate, self).post(request, *args, **kwargs)


# 	def get_context_data(self, **kwargs):
# 		context['form'] = self.form
# 		return context




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

