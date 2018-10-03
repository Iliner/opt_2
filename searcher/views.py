from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import *
# Create your views here.





class SearchInput(TemplateView):
	template_name = 'main_page/index.html'
	form = None

	def get(self, request, *args, **kwargs):
		self.form = SeacerForm
		return super(SearchInput, self).get(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if self.form.is_valid():
			print('search form')
		else:
			return super(SearchInput, self).post(request, *args, **kwargs)






def searche_good(request):
	if request.method == "POST":
		print('search', request.POST['value'])
	ro = 2
	return HttpResponse(ro)

