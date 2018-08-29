from django.conf.urls import url 
#from main_page import views
from main_page.twviews import *


urlpatterns = [
	url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name='index'),
	url(r'good/(?:(?P<code>\d+)/)$', GoodDetailView.as_view(), name='good_page'),
	url(r'^(?P<cat_id>\d+)/add/$', GoodCreate.as_view(), name='good_add'),
	url(r'^good/(?P<code>\d+)/edit/$', GoodUpdate.as_view(), name='good_edit'),
	url(r'^good/(?P<code>\d+)/delete/$', GoodDelete.as_view(), name='good_delete'),
	url(r'^add_file/$', AddFiles.as_view(), name='add_file'),

]