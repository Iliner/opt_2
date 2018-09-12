from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.views.generic.base import ContextMixin
from django.views.generic.detail import DetailView
from django.core.urlresolvers import reverse
from django import forms
from .models import * 
from django.core.exceptions import ValidationError


def valid_positive(value):
	if value < 0:
		raise ValidationError('Значение должно быть больше 0', code='invalid')



class GoodForm(forms.ModelForm):
	class Meta:
		model = Goods
		fields = "__all__"
		#fields = ['code', 'articul', 'producer', 'description', 'price']
		# labels = {'code': 'код', 'articul': 'артикул', 'producer': 'производитель', 'description': 'описание', 'price': 'стоймость'}

	code = forms.IntegerField(label = 'код', help_text='Кож товара', error_messages={'required': 'блаб балаб лабла'}, validators=[valid_positive])
	articul = forms.CharField(label = 'артикул', help_text='артикул')
	producer = forms.CharField(label = 'произврдитель', help_text='имя производителя')
	description = forms.CharField(label = 'описание', help_text='Описание товара', widget=forms.Textarea)
	price = forms.IntegerField(label = 'цена', help_text='Стоймость товара')
	category = forms.ModelChoiceField(queryset=Category.objects.order_by('name')) 



class CustomerStock(forms.Form):
	count = forms.IntegerField()



class UploadFiles(forms.ModelForm):
	class Meta:
		model = FileUpload
		fields = "__all__"

	name = forms.CharField(label = 'Название файла', help_text='Название товара которое будет отображаться в меню админа', 
		error_messages={'required': 'блаб балаб лабла'})
	file = models.FileField(help_text='Название товара которое будет отображаться в меню админа')




class UploadImg(forms.ModelForm):
	class Meta:
		model = UploadsImage
		fields = '__all__'