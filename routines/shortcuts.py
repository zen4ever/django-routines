def render_response(req, *args, **kwargs):
        """
        Helper method which passes RequestContext to templates instead of plain Context.
        Passes some additional variables to templates
        """
        from django.shortcuts import render_to_response
        from django.template import RequestContext
        kwargs['context_instance'] = RequestContext(req)
        return render_to_response(*args, **kwargs)

