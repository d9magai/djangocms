from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic.base import RedirectView


class LogoutView(RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse('owner:login')

    def dispatch(self, request, *args, **kwargs):
        try:
            logout(request)
        except:
            # if we can't log the user out, it probably means they we're not
            # logged-in to begin with, so we do nothing
            pass
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


def index(request):
    return render(request, 'owner/index.html')


@login_required(login_url='/owner/login/')
def mypage(request):
    return render(request, 'owner/mypage.html')


@login_required(login_url='/owner/login/')
def redirect(request):
    return render(request, 'owner/redirect.html')
