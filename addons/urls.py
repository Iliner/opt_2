from django.conf.urls import url 
#from main_page import views
from .views import *
from .excel_views import *
from django.contrib.auth.decorators import login_required, permission_required


# app_name = 'shopping_cart'

urlpatterns = [
	url(r'working_excel', working_excel, name='working_excel'),
	url(r'^banners/$', BannerView.as_view(), name='banners_view'),
	url(r'^excel_download/$', ExcelDownload.as_view(), name='download_excel'),
	url(r'^catalog_pdf/$', CatalogImgView.as_view(), name='catalog_pdf'), 
	url(r'^catalog_pdf_open/(?P<catalog_id>\d+)/$', CatalogOpenView.as_view(), name='catalog_pdf_open'),
	url(r'hidden_opt', hidden_opt, name='hidden_opt') 
]