from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'owner/index.html')
 
 
@login_required(login_url='/owner/login/')
def mypage(request):
    return render(request, 'owner/mypage.html')
 
 
@login_required(login_url='/owner/login/')
def redirect(request):
    return render(request, 'owner/redirect.html')
