from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from django.core.paginator import Paginator, InvalidPage
# Create your views here.




def index(request, cat_id):
	cat= None
	try:
		page_num = request.GET['page']
	except KeyError:
		page_num = 1
	cats = Category.objects.all()
	if cat_id:
		category = Category.objects.get(pk=cat_id)
		pag = Paginator(Goods.objects.filter(category=category), 1)
		cat = category
		try:
			goods = pag.page(page_num)
		except InvalidPage:
			goods = pag.page(1)
	else:
		pag = Paginator(Goods.objects.all(), 1)
		try:
			goods = pag.page(page_num)
		except InvalidPage:
			goods = pag.page(1)
	if cat:
		return render(request, "main_page/list_goods.html", {'goods': goods,  'cats': cats, 'page': page_num, 'category': cat})
	else:
		return render(request, "main_page/list_goods.html", {'goods': goods,  'cats': cats, 'page': page_num,})




def good_page(request, code):
	try:
		good = Goods.objects.get(code=code)
	except Good.DoesNotExist as err:
		raise Http404
	else: 
		return render(request, "main_page/good_page.html", {'good': good})
	




# def index(request, id):
# 	cat = request.GET
# 	good = Goods.objects.filter(category__name__startswith = 'Лесное')
# 	category = Category.objects.get(name='Гаражное оборудование')
# 	g_c = category.goods_set.all()
# 	return HttpResponse(g_c)
# 	