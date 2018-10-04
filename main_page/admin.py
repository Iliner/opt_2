from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)

@admin.register(Goods)
class AdminGoods(admin.ModelAdmin):
	list_display = ['code', 'articul', 'price']

#admin.site.register(Goods)
admin.site.register(Photo)
admin.site.register(UploadsImage)
admin.site.register(FileUpload)
admin.site.register(Producers)
admin.site.register(NewGoods)
# admin.site.register(OrderItem)
# admin.site.register(Order)
# admin.site.register(Profile)

