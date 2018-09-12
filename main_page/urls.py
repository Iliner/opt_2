from django.conf.urls import url 
#from main_page import views
from main_page.twviews import *
from django.contrib.auth.decorators import login_required, permission_required


# app_name = 'shopping_cart'

urlpatterns = [
	url(r'^(?:(?P<cat_id>\d+)/)?$', GoodListView.as_view(), name='index'),
	url(r'good/(?:(?P<code>\d+)/)$', GoodDetailView.as_view(), name='good_page'),
	url(r'^(?P<cat_id>\d+)/add/$', GoodCreate.as_view(), name='good_add'),
	url(r'^good/(?P<code>\d+)/edit/$', permission_required('main_page.change_good', GoodUpdate.as_view()), name='good_edit'),
	url(r'^good/(?P<code>\d+)/delete/$', GoodDelete.as_view(), name='good_delete'),
	url(r'^add_file/$', login_required(AddFiles.as_view()), name='add_file'),
	url(r'^add_img/$', uploads_photo, name='add_img'),

    # url(r'^add-to-cart/(?P<item_id>[-\w]+)/$', add_to_cart, name="add_to_cart"),
    # url(r'^order-summary/$', order_details, name="order_summary"),
    # url(r'^success/$', success, name='purchase_success'),
    # url(r'^item/delete/(?P<item_id>[-\w]+)/$', delete_from_cart, name='delete_item'),
    # url(r'^checkout/$', checkout, name='checkout'),
    # url(r'^update-transaction/(?P<token>[-\w]+)/$', update_transaction_records,
    #     name='update_records')
]