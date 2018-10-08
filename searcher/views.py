from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import *
from django.views.decorators.csrf import csrf_exempt
from main_page.models import Goods
from main_page.models import Photo

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
							<div class='search_output_producer'>{producer}</div>
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
	print(result_str)
	return HttpResponse(result_str)