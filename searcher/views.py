from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from main_page.models import Goods
# Create your views here.





class SearchInput(TemplateView):
	template_name = 'main_page/index.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = SeacerForm
		return super(SearchInput, self).get(request, *args, **kwargs)




@csrf_exempt
def searche_good(request):
	if request.method == "POST":
		query = request.POST.get('input_data')
		goods = Goods.objects.all()
		search_articles = goods.filter(code=query)
		result = goods.filter(
			Q(code__icontains=query)|
			Q(articul__icontains=query)
			).distinct()

		print('search', result)
	ro = 2
	return HttpResponse(ro)

