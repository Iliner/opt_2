from django.conf.urls import url 
from .views import *




urlpatterns = [
	url(r'^filter/1/(?P<category_id>\d+)/$', FilterLvlOne.as_view(), name='filter_request_one'),
	url(r'^filter/2/(?P<category_id>\d+)/$', FilterLvlTwo.as_view(), name='filter_request_two'),
	url(r'^filter/3/(?P<category_id>\d+)/$', FilterLvlThree.as_view(), name='filter_request_three'),
	url(r'^filter/4/(?P<category_id>\d+)/$', FilterLvlFour.as_view(), name='filter_request_four'),
	url(r'^filter/5/(?P<category_id>\d+)/$', FilterLvlFive.as_view(), name='filter_request_five'),
	
]