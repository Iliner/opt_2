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


@register.filter
def counter_stock(value=1):
	return int(value)


def do_ivan(parser, token):
    nodelist = parser.parse(('endcomment',))
    parser.delete_first_token()
    return CommentNode()

class IvanNode(template.Node):
    def render(self, context):
        return 