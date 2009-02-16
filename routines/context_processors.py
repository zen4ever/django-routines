def current_site(request):
    from django.contrib.sites.models import Site
    try:
        site = Site.objects.get_current()
        return {
            'site': site
            }
    except Site.DoesNotExist:
        return {'site': ''}

def static_media(request):
    from django.conf import settings
    url = settings.STATIC_URL
    return {'STATIC_URL': url}

