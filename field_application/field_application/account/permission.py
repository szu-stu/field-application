from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

def guest_or_redirect(function=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated(),
        login_url='/',
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def check_user_pk(function=None):
    def decorator(function):
        def wrapped_check(request, *args, **kwargs):
            if not kwargs.get('pk'):
                raise Exception('url in urls.py need "(?P<pk>\d+)"')
            if request.user.pk != int(kwargs.get('pk')):
                return HttpResponseRedirect(reverse('deny'))
            kwargs['pk'] = request.user.organization.pk
            return function(request, *args, **kwargs)
        return wrapped_check
    return login_required(decorator(function))
