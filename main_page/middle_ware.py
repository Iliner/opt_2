from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse




class AuthRequiredMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.process_request(request)

	def process_request(self, request):
		if not request.user.is_authenticated():
			return HttpResponseRedirect(reverse('login')) # or http response
		none = None
		return HttpResponse(request.GET['url'])