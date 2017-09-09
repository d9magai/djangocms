from __future__ import absolute_import

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import FormView
from .forms import LoginForm
from .forms import RegistrationForm


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('owner:mypage')
    template_name = 'owner/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


def index(request):
    return render(request, 'owner/index.html')


@login_required(login_url='/owner/login/')
def mypage(request):
    return render(request, 'owner/mypage.html')


@login_required(login_url='/owner/login/')
def redirect(request):
    return render(request, 'owner/redirect.html')
