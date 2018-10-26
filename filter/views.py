from django.shortcuts import render
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.views.generic.base import ContextMixin

from .models import *
from main_page.models import Goods
from main_page.models import Photo
from basket.models import Cart
from basket.models import Manager
from basket.forms import CartItemCount




class CategoryListMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CategoryListMixin, self).get_context_data(**kwargs)
		context['default_img'] = Photo.objects.get(name="Default").photo
		context['opt_status'] = self.opt_status
		dict_count = {}
		for items in self.cart.items.all():
			dict_count[items.product.code] = items.count
		context['dict_count'] = dict_count
		return context



class CommonGet(View):
	
	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		print('id', self.category_id)
		return super(CommonGet, self).get(request, *args, **kwargs)


class FilterLvlOne(ListView, CategoryListMixin):
	template_name = 'filter/result.html'
	paginate_by = 100
	category_id = None
	cat = None
	form = None
	cart = None
	opt_user = None
	customer = None
	opt_status = None

	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		try:
			print("request.session['search_query']", request.session['search_query'])
		except:
			print("request.session['search_query']", 'netu')
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()	
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')		
		if self.customer.baskets.filter(paid_for=False).exists():
			for basket in self.customer.baskets.all():
				if not basket.paid_for:
					self.cart = basket
					request.session['cart_id'] = basket.id
					request.session['goods_card'] = dict()
		else:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.customer.baskets.add(cart)
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		self.form = CartItemCount
		self.opt_status = request.session.get('opt_status')
		return super(FilterLvlOne, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FilterLvlOne, self).get_context_data(**kwargs)
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context

	def get_queryset(self): 
		return Goods.objects.filter(filter_lvl_one__id=self.category_id)


class FilterLvlTwo(ListView, CategoryListMixin):
	template_name = 'filter/result.html'
	paginate_by = 100
	category_id = None
	cat = None
	form = None
	cart = None
	opt_user = None
	customer = None
	opt_status = None

	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		try:
			print("request.session['search_query']", request.session['search_query'])
		except:
			print("request.session['search_query']", 'netu')
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()	
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')		
		if self.customer.baskets.filter(paid_for=False).exists():
			for basket in self.customer.baskets.all():
				if not basket.paid_for:
					self.cart = basket
					request.session['cart_id'] = basket.id
					request.session['goods_card'] = dict()
		else:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.customer.baskets.add(cart)
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		self.form = CartItemCount
		self.opt_status = request.session.get('opt_status')
		return super(FilterLvlTwo, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FilterLvlTwo, self).get_context_data(**kwargs)
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context
			
	def get_queryset(self): 
		return Goods.objects.filter(filter_lvl_two__id=self.category_id)

class FilterLvlThree(ListView, CategoryListMixin):
	template_name = 'filter/result.html'
	paginate_by = 100
	category_id = None
	cat = None
	form = None
	cart = None
	opt_user = None
	customer = None
	opt_status = None

	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		try:
			print("request.session['search_query']", request.session['search_query'])
		except:
			print("request.session['search_query']", 'netu')
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()	
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')		
		if self.customer.baskets.filter(paid_for=False).exists():
			for basket in self.customer.baskets.all():
				if not basket.paid_for:
					self.cart = basket
					request.session['cart_id'] = basket.id
					request.session['goods_card'] = dict()
		else:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.customer.baskets.add(cart)
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		self.form = CartItemCount
		self.opt_status = request.session.get('opt_status')
		return super(FilterLvlThree, self).get(request, *args, **kwargs)
	
	def get_context_data(self, **kwargs):
		context = super(FilterLvlThree, self).get_context_data(**kwargs)
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context

	def get_queryset(self): 
		return Goods.objects.filter(filter_lvl_three__id=self.category_id)



class FilterLvlFour(ListView, CategoryListMixin):
	template_name = 'filter/result.html'
	paginate_by = 100
	category_id = None
	cat = None
	form = None
	cart = None
	opt_user = None
	customer = None
	opt_status = None

	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		try:
			print("request.session['search_query']", request.session['search_query'])
		except:
			print("request.session['search_query']", 'netu')
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()	
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')		
		if self.customer.baskets.filter(paid_for=False).exists():
			for basket in self.customer.baskets.all():
				if not basket.paid_for:
					self.cart = basket
					request.session['cart_id'] = basket.id
					request.session['goods_card'] = dict()
		else:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.customer.baskets.add(cart)
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		self.form = CartItemCount
		self.opt_status = request.session.get('opt_status')
		return super(FilterLvlFour, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FilterLvlFour, self).get_context_data(**kwargs)
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context

	def get_queryset(self): 
		return Goods.objects.filter(filter_lvl_four__id=self.category_id)


class FilterLvlFive(ListView, CategoryListMixin):
	template_name = 'filter/result.html'
	paginate_by = 100
	category_id = None
	cat = None
	form = None
	cart = None
	opt_user = None
	customer = None
	opt_status = None

	def get(self, request, *args, **kwargs):
		self.category_id = kwargs['category_id']
		try:
			print("request.session['search_query']", request.session['search_query'])
		except:
			print("request.session['search_query']", 'netu')
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()	
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')		
		if self.customer.baskets.filter(paid_for=False).exists():
			for basket in self.customer.baskets.all():
				if not basket.paid_for:
					self.cart = basket
					request.session['cart_id'] = basket.id
					request.session['goods_card'] = dict()
		else:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.customer.baskets.add(cart)
			request.session['cart_id'] = cart_id
			self.cart = Cart.objects.get(id=cart_id)
		self.form = CartItemCount
		self.opt_status = request.session.get('opt_status')
		return super(FilterLvlFive, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(FilterLvlFive, self).get_context_data(**kwargs)
		context['cart'] = self.cart
		context['form'] = self.form
		context['opt_user'] = self.opt_user
		return context

	def get_queryset(self): 
		return Goods.objects.filter(filter_lvl_five__id=self.category_id)		