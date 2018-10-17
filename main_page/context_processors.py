from main_page.models import Producers
from django.views.generic.list import ListView
from main_page.twviews import * 

def producers_book(request):
	context = {}
	context['producers_books'] = Producers.objects.filter(visibility=True).order_by('rating')
	return context




def producers_all_navbar(request):
	context = {}
	context['producers_all_navbar'] = Producers.objects.order_by('name')
	return context


def users_manager(request):
		context = {}
		try:
			customer = request.user.customer_set.first()
			opt_user = request.user.customer_set.first().opt
		except Exception as err:
			print(err)
		try:
			manager = Manager.objects.get(customers=customer)
			context['manager_first_name'] = manager.first_name
			context['manager_last_name'] = manager.last_name
			context['manager_mail_work'] = manager.mail_work
			context['manager_phone_number_work'] = manager.phone_number_work
		except Exception as err:
			print(err)
		return context
