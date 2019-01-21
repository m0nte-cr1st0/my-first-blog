from django import template
from post.models import Post
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('post/search_tpl.html', takes_context=True)
def search(context):
    request = context['request']
    query = request.GET.get('q')  # removed self. That was causing the proble
    founded = Post.objects.filter(Q(title__icontains=query)|Q(body__icontains=query))
    return {'founded': founded}
