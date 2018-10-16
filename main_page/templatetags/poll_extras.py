from django import template
from django.http import HttpResponse
from main_page.models import *


register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return int(value) % int(arg)
    except (ValueError, ZeroDivisionError):
        return None


# @register.filter
# def forsage(reqvest): 
# 	good = Goods.objects.first().producer.name
# 	return good