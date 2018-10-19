import re

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.base import ContextMixin
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from main_page.models import *
from basket.models import Cart
from basket.forms import CartItemCount
from functools import reduce
import operator


class CategoryListMixin(ContextMixin):
	def get_context_data(self, **kwargs):
		context = super(CategoryListMixin, self).get_context_data(**kwargs)
		context['cats'] = Category.objects.order_by('name')
		context['default_img'] = Photo.objects.get(name="Default").photo

		dict_count = {}
		for items in self.cart.items.all():
			dict_count[items.product.code] = items.count
		context['dict_count'] = dict_count 

		return context

class SearchInput(TemplateView):
	template_name = 'search/search_input.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = SeacerForm
		return super(SearchInput, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):	
		context['form'] = self.form
		return context



@csrf_exempt
def searche_good(request, query_full=None):
	print('i work')
	query = request.POST.get('input_data')
	result_str = ""
	if request.POST.get('input_data'):
		request.session['search_query'] = request.POST.get('input_data')

	if request.method == "POST" and not query_full:
		query = request.POST.get('input_data')

		# idseq = request.POST.get('input_data').split()
		# print('idseq', idseq)
		# tag_qs = reduce(operator.or_, (Q(code=x) for x in idseq))
		# print('tag_qs', tag_qs)
		# result = Goods.objects.filter(..., tag_qs)
		# print(result)

		# goods = Goods.objects.all()
		# search_articles = goods.filter(code=query)
		# result = goods.filter(
		# 	Q(code__icontains=query)|
		# 	Q(articul__icontains=query) 
		# 	).distinct()[:10]


		# or_lookup = (
		# 	Q(code__icontains=query)|
		# 	Q(articul__icontains=query)
		# 	)
		# result = Goods.objects.filter(or_lookup).distinct()[:10]
		
		
		# idseq = request.POST.get('input_data').split()
		# result = Goods.objects.filter(
		# 	code__icontains=query,
		# 	articul__icontains=query
		# 	).distinct()[:10]


		query_string = ''
		found_entries = None
		query_string = request.POST.get('input_data')
		entry_query = get_query(query_string, ['code', 'articul', 'description'])
		result = Goods.objects.filter(entry_query).distinct()[:10]
		for good in result:
			try:
				photo_url = good.photo.photo.url
			except:
				photo_url = Photo.objects.get(name='Default').photo.url

			link = """
			<div class='search_output_row'>
				<a href='/good/{code}/'>
				<div class='search_output_wrapper'>
					<div class='search_output_row_img'><img src='{src}'></div>
					<div class='search_output_wrapper_data'>
						<div class='search_output_characteristics'>
							<div class='search_output_producer'>{producer.name}</div>
							<div class='search_output_articul'>{articul}</div>
							<div class='search_output_code'>{code}</div>
						</div>
						<div class='search_output_description'>{description}</div>
					</div>
				</div>
				</a>
			</div>
			""".format(
				code=good.code,
				producer=good.producer, 
				articul=good.articul, 
				description=good.description,
				src=photo_url
				)
			result_str += link

		return HttpResponse(result_str)

	if query_full:

		query_string = ''
		found_entries = None
		query_string = query_full
		entry_query = get_query(query_string, ['code', 'articul', 'description'])
		result = Goods.objects.filter(entry_query).distinct()
		return result


def normalize_query(
	query_string,
    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
    normspace=re.compile(r'\s{2,}').sub):

    return [normspace('',(t[0] or t[1]).strip()) for t in findterms(query_string)]


def get_query(query_string, search_fields):
    query = None 
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query	
    return query








class SearchGoodsFull(ListView, CategoryListMixin):
	template_name = 'search/search_full_list.html'
	paginate_by = 100
	form = None
	cart = None
	opt_user = None
	customer = None
	list_goods = None 
	cat = None

	def get(self, request, *args, **kwargs):
		print('i work two')
		print('.;', request.session['search_query'])
		if request.user.is_authenticated():
			try:
				self.customer = request.user.customer_set.first()
				self.opt_user = request.user.customer_set.first().opt
			except Exception as err:
				print(err)
		else:
			return redirect('login')

		if self.customer.baskets.all().exists():
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

		query = request.session['search_query']
		print('asdasd', query)	 	
		if query:
			self.list_goods = searche_good(request, query_full=query)
			print('self.list_goods', self.list_goods)


		return super(SearchGoodsFull, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		"""
		Создает контекст данных
		"""

		# Формирует сам контекст данных и заполнит его начальными данными, 
		# в частности значениями полученными контроллером параметров.

		context = super(SearchGoodsFull, self).get_context_data(**kwargs) 
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


		return self.list_goods


	def post(self, request, *args, **kwargs):
		if self.form.is_valid():
			self.form.save()
		else:
			return super(SearchGoodsFull, self).post(request, *args, **kwargs)