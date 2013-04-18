from django import template
from django.core import urlresolvers
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('tags/edit_list.html')
def edit_list(instance, link=None):
    if not link:
        link = 'edit in admin'
    content_type = ContentType.objects.get_for_model(instance.__class__)
    admin_url = urlresolvers.reverse("admin:%s_%s_change" % (content_type.app_label, content_type.model), args=(instance.pk,))

    return dict(link=link, admin_url=admin_url)
