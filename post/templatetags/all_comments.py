from django import template
from post.models import Comment
from django.core.paginator import Paginator
register = template.Library()

@register.inclusion_tag('post/comment_list.html')
def comment_list(page_number=1):
    comments = Comment.objects.filter()[0:25]
    current_page = Paginator(comments, 5)
    return {'comments': current_page.page(page_number)}

from datetime import timedelta

import online_users.models


@register.inclusion_tag('post/online_users.html')
def see_users():
  user_status = online_users.models.OnlineUserActivity.get_user_activities(timedelta(seconds=60))
  users_count = user_status.all().count()
  users = (user for user in  user_status)
  return {'users': users, 'users_count': users_count}

from django.utils.http import is_safe_url, urlunquote
from django.conf import settings
import geoip2.database
import requests

from django.template import RequestContext

PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', )
@register.inclusion_tag('post/weather_tpl.html', takes_context=True)
def city_weather(context):
    request = context['request']
    remote_address = request.META.get('REMOTE_ADDR')
    ip = remote_address
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        proxies = x_forwarded_for.split(',')
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]

    reader = geoip2.database.Reader('post/GeoLite2-City_20190108/GeoLite2-City.mmdb')
    try:
        city = reader.city(ip).city.name
    except:
        city = 'Dnipro'

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&lang=ru&appid=4e328f5a34221d8b56cc9e2f55417a76'
    city_weather = requests.get(url.format(city)).json()

    weather = {
        'city' : city,
        'temperature' : str(city_weather['main']['temp'])+'°C,',
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    next = request.META.get('HTTP_REFERER')
    if next:
        next = urlunquote(next)  # HTTP_REFERER may be encoded.
    if not is_safe_url(url=next, allowed_hosts={request.get_host()}):
        next = '/'
    return {'next': next, 'city': city, 'weather' : weather }
