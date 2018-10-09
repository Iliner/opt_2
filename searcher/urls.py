from django.conf.urls import url 
from searcher.views import *
from django.contrib.auth.decorators import login_required, permission_required

urlpatterns = [
	url(r'searche_good$', searche_good, name='searche_good'),
]