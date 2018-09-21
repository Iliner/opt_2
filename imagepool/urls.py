from django.conf.urls import url, include
from  imagepool.views import get_list
# Create your views here.


# urlpatterns = [
# 	url(r'^$',  views.index, name='index'),
# 	url(r"^good/(?P<code>\d+)/$", views.good, name='good'),
# ]

urlpatterns = [
	url(r"^imagepool/$",  get_list, name='file_lister'),
]