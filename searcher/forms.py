from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import ModelForm
from .models import * 



# class SeacerForm(forms.Form):
# 	searcher = forms.CharField()



class SeacerForm(forms.ModelForm):
	class Meta:
		model = SearchUserQuery
		fields = "__all__"
