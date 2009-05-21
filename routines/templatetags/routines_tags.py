from django import template
import urlparse
import os.path
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()

@register.filter
def startswith(value, arg):
    """ Usage, {% if value|starts_with:"arg" %}"""
    return value.startswith(arg)

@register.filter
def truncatechars(s, num=15):
    length = int(num)
    string = []
    for word in s.split():
        if len(word) > length:
            string.append(word[:length]+'...')
        else:
            string.append(word)
    return u' '.join(string)

def _absolute_url(url):
    if url.startswith('http://') or url.startswith('https://'):
        return url
    domain = Site.objects.get_current().domain
    return 'http://%s%s' % (domain, url)

@register.simple_tag
def static(filename, flags=''):
    """
    Handles urls to static files, adds timestamp to js and css files.
    Taken from Ivan Salagaev http://softwaremaniacs.org/ 
    """
    flags = set(f.strip() for f in flags.split(','))
    url = urlparse.urljoin(settings.STATIC_URL, filename)
    if 'absolute' in flags:
        url = _absolute_url(url)
    if (filename.endswith('.css') or filename.endswith('.js')) and 'no-timestamp' not in flags or \
       'timestamp' in flags:
        fullname = os.path.join(settings.STATIC_ROOT, filename)
        if os.path.exists(fullname):
            url += '?%d' % os.path.getmtime(fullname)
    return url

@register.simple_tag
def gravatar(email, size=49, default="identicon"):
    from django.utils.hashcompat import md5_constructor
    import urllib
    from django.utils.html import escape
    url = "http://www.gravatar.com/avatar/%s/?" % md5_constructor(email).hexdigest()
    url += urllib.urlencode({"s": str(size), "default": default})
    return escape(url)

@register.filter
def localeformat(value, format):
    import locale
    locale.setlocale(locale.LC_ALL, "")
    return locale.format("%"+format, value, True) 

