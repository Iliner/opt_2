from django import template
from django.http import HttpResponse
from main_page.models import *

from django.template import Context, RequestContext, Template
from django.core.paginator import Paginator
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


def render_template(value, **context):
    template = Template(value)

    request = context.get('request')
    ctx = RequestContext(request, context) if request else Context(context)
    return template.render(ctx).strip()


def test_paginate_first():
    objects = ['foo'] * 50
    paginator = Paginator(objects, 1)
    page = paginator.page(1)

    content = render_template(
        "{% load rangepaginator %}{% paginate page %}",
        page=page)
    assert content


def test_paginate_last():
    objects = ['foo'] * 50
    paginator = Paginator(objects, 1)
    page = paginator.page(50)

    content = render_template(
        "{% load rangepaginator %}{% paginate page %}",
        page=page)
    assert content


def test_paginate_with_request_first(rf):
    request = rf.get('/', data={'foo': 'bar'})
    objects = ['foo'] * 50
    paginator = Paginator(objects, 1)
    page = paginator.page(1)

    content = render_template(
        "{% load rangepaginator %}{% paginate page request=request %}",
        page=page, request=request)
    assert content
    assert 'foo=bar' in content


def test_paginate_with_request_last(rf):
    request = rf.get('/', data={'foo': 'bar'})
    objects = ['foo'] * 50
    paginator = Paginator(objects, 1)
    page = paginator.page(50)

    content = render_template(
        "{% load rangepaginator %}{% paginate page request=request %}",
        page=page, request=request)
    assert content
    assert 'foo=bar' in content
