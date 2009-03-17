from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils.cache import patch_vary_headers
import datetime

class DualSessionMiddleware(object):
    """Session middleware that allows you to turn individual browser-length 
    sessions into persistent sessions and vice versa.

    This middleware can be used to implement the common "Remember Me" feature
    that allows individual users to decide when their session data is discarded.
    If a user ticks the "Remember Me" check-box on your login form create
    a persistent session, if they don't then create a browser-length session.

    This middleware replaces SessionMiddleware, to enable this middleware:
    - Add this middleware to the MIDDLEWARE_CLASSES setting in settings.py, 
    replacing the SessionMiddleware entry.
    - In settings.py add this setting: 
    PERSISTENT_SESSION_KEY = 'sessionpersistent'    - Tweak any other regular SessionMiddleware settings (see the sessions doc),
    the only session setting that's ignored by this middleware is 
    SESSION_EXPIRE_AT_BROWSER_CLOSE. 

    Once this middleware is enabled all sessions will be browser-length by
    default.

    To make an individual session persistent simply do this:

    session[settings.PERSISTENT_SESSION_KEY] = True

    To make a persistent session browser-length again simply do this:

    session[settings.PERSISTENT_SESSION_KEY] = False
    """

    def process_request(self, request):
        engine = __import__(settings.SESSION_ENGINE, {}, {}, [''])
        request.session = engine.SessionStore(request.COOKIES.get(settings.SESSION_COOKIE_NAME, None))

    def process_response(self, request, response):
        # If request.session was modified, or if response.session was set, save
        # those changes and set a session cookie.
        patch_vary_headers(response, ('Cookie',))
        try:
            modified = request.session.modified
        except AttributeError:
            pass
        else:
            if modified or settings.SESSION_SAVE_EVERY_REQUEST:
                session_key = request.session.session_key or Session.objects.get_new_session_key()

                if not request.session.get(settings.PERSISTENT_SESSION_KEY, False):
                    # session will expire when the user closes the browser
                    max_age = None
                    expires = None
                else:
                    max_age = settings.SESSION_COOKIE_AGE
                    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE), "%a, %d-%b-%Y %H:%M:%S GMT")

                new_session = Session.objects.save(session_key,
                                                   request.session._session,
                                                   datetime.datetime.now() + datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE))

                response.set_cookie(settings.SESSION_COOKIE_NAME, session_key,
                                    max_age = max_age, expires = expires,
                                    domain = settings.SESSION_COOKIE_DOMAIN,
                                    secure = settings.SESSION_COOKIE_SECURE or None)
        return response

