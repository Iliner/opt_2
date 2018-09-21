from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelForm
from .models import * 




# class Order(forms.ModelForm):
# 	class Meta:
# 		model = Goods
# 		fields = ['order_count']
# 	order_count = forms.IntegerField(label = False, min_value=0, max_value=100, validators=[MinValueValidator('0')], widget=forms.NumberInput(attrs={'style': 'width: 55px'}))


class CartItemCount(forms.ModelForm):
	
	
	class Meta:
		model = CartItem
		fields = ['count']
	count = forms.IntegerField(initial=1, label = False, min_value=0, max_value=100, validators=[MinValueValidator('0')], widget=forms.NumberInput(attrs={'style': 'width: 55px'}))


