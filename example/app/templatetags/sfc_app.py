from django import template

from sfc.templatetags.sfc import load

register = template.Library()

register.simple_tag(func=load('sfc/app/list.html'), name='list')

register.simple_tag(func=load('sfc/app/dropdown.html'), name='dropdown')

