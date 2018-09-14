from django.conf.urls import url, include
from basket.views import CartView, add_to_card_view, DeletePosition
# Create your views here.


# urlpatterns = [
# 	url(r'^$',  views.index, name='index'),
# 	url(r"^good/(?P<code>\d+)/$", views.good, name='good'),
# ]

urlpatterns = [
	url(r"^add_to_card/(?P<code>\d+)/$",  add_to_card_view, name='add_cart'),
	url(r"^cart/$", CartView.as_view(), name='cart' ),
	url(r"^cart/(?P<pk>\d+)?$", DeletePosition.as_view(), name='cart_delete_positon' ),
]