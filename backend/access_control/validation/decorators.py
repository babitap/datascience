from functools import wraps
from urllib.parse import urlparse

from django.shortcuts import resolve_url
from django.contrib.auth import REDIRECT_FIELD_NAME


def custom_user_passes_test(test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):

            #Split requets components
            user=request.user
            request=request.request

            #Check function
            if test_func(user):
                return view_func(request, *args, **kwargs)

            #Build return output
            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def custom_permission_required(*perms, redirect_field_name=REDIRECT_FIELD_NAME, login_url='/'):

    return custom_user_passes_test(
        lambda u: u.is_active and any(u.has_perm(perm) for perm in perms), 
        login_url=login_url,
        redirect_field_name=redirect_field_name
        )
