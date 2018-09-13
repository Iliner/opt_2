from django.conf.urls import url, include
from basket.views import cart_view, add_to_card_view
# Create your views here.


# urlpatterns = [
# 	url(r'^$',  views.index, name='index'),
# 	url(r"^good/(?P<code>\d+)/$", views.good, name='good'),
# ]

urlpatterns = [
	url(r"^/add_to_card/(?P<code>\d+)/$",  add_to_card_view, name='add_cart'),
	url(r"^cart/$", cart_view, name='cart' ),
]