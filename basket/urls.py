from django.conf.urls import url, include
from basket.views import *
# Create your views here.


# urlpatterns = [
# 	url(r'^$',  views.index, name='index'),
# 	url(r"^good/(?P<code>\d+)/$", views.good, name='good'),
# ]

urlpatterns = [
	url(r"^add_to_card/(?P<code>\d+)/$",  add_to_card_view, name='add_cart'),
	url(r"^cart/$", CartView.as_view(), name='cart' ),
	url(r"^cart/(?P<pk>\d+)?$", DeletePosition.as_view(), name='cart_delete_positon' ),
	url(r'^delete_from_cart_view/(?P<code>\d+)?$', delete_from_cart_view, name='delete_from_cart_view'),
	url(r'count/add', add_view, name='add_to_card'),
	url(r'count/delete', delete_item, name='delete_item'),
	url(r'confirm/order', confirm_order, name='confirm_order'),
	url(r"^history_order/$",  HistoryOrderView.as_view(), name='history_order'),
]