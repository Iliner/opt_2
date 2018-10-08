from django.conf.urls import url, include
from .views import *


urlpatterns = [
	url(r'download_photo', download_photo_view, name='download_photo'),
]