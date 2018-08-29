from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Goods)
admin.site.register(Photo)
admin.site.register(UploadsImage)
admin.site.register(FileUpload)