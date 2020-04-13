from django import template
from django.conf import settings
from django.template import Template, Context
from django.template.loader import get_template
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from sfc.register import registry

register = template.Library()


def load(tpl):
    template = get_template(tpl).template
    registry.register(template)

    def wrapped_f(**kwargs):
        registry.queue.add(template.name)
        html = registry.get_html(tpl)
        return Template(html).render(Context(kwargs))

    return wrapped_f


@register.simple_tag
def sfc_css():
    css = registry.templates.values()

    if settings.SFC_COMPILE == "inline":
        css = "\n".join([x.css.render() for x in css])
        css = f"<style>\n{css}\n</style>"
    else:
        link = "<link rel='stylesheet' href='{name}.css' />"
        css = "\n".join([link.format(name=static(x.file_name)) for x in css])

    return mark_safe(css)


@register.simple_tag
def sfc_js():
    tpls = [t for name, t in registry.templates.items() if name in registry.queue]
    tags = f"<script type='module' src='{static('sfc/component.js')}'></script>"
    js = [f"var tpl = `{t.html.render()}`\n{t.js.render()}" for t in tpls]

    if settings.SFC_COMPILE == "inline":
        js = "\n".join(js)
        tags += f"<script type='module'>\n{js}\n</script>"
    else:
        link = "<script type='module' src='{name}.js'></script>"
        tags += "\n".join([link.format(name=static(x.file_name)) for x in tpls if x.js.render()])
    registry.queue = set()
    return mark_safe(tags)
