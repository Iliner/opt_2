from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse




class AuthRequiredMiddleware:

	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		return self.process_request(request)

	def process_request(self, request):
		print(request.get_full_path())
		print(request.COOKIES.get('sessionid'))
		if not request.user.is_authenticated() and request.get_full_path() != '/login/':
			return HttpResponseRedirect(reverse('login')) # or http response
		if request.COOKIES.get('sessionid'):
			none = None
			return HttpResponse(none)