from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from main_page.models import Goods

# Create your views here.





class SearchInput(TemplateView):
	template_name = 'search/search_input.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = SeacerForm
		return super(SearchInput, self).get(request, *args, **kwargs)

	def get_context_data(self, **kwargs):	
		context['form'] = self.form
		return context




def searche_good(request):
	query = request.POST.get('input_data')
	print('balbal')
	print(query)
	result_str = ""
	if request.method == "POST":
		query = request.POST.get('input_data')
		print(query)
		goods = Goods.objects.all()
		search_articles = goods.filter(code=query)
		result = goods.filter(
			Q(code__icontains=query)|
			Q(articul__icontains=query) 
			).distinct()[:10]
		print('search', result)
		for good in result:
			link = "<div class='search_output_row'><a href='/good/{}/'>{} {}</a></div>".format(good.code, good.code, good.producer)
			result_str += link
	print(result_str)
	return HttpResponse(result_str)