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



# {% block books_producers%}
# 	<div id='books_producers_wrapper'>
# 	{% for producer in producers %}
# 		<div id='books_producers_producer'><a href="{% url 'producer_list' id=producer.id %}" class='books_producers_producer_link'>{{producer.name}}</a></div>
# 	{% endfor %}
# 	</div>
# {% endblock %}