from django.utils import simplejson as json
from django.http import HttpResponse

def ajax_login_required(response_type, response=None):
    def actual_decorator(view_func):
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            if response_type=="html":
                result = response or 'You need to login'
                return HttpResponse(result, mimetype="text/html")
            result = json.dumps({ 'not_authenticated': True })
            return HttpResponse(result, mimetype='application/json')
        wrap.__doc__ = view_func.__doc__
        wrap.__dict__ = view_func.__dict__
        return wrap
    return actual_decorator

