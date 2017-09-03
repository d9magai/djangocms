"""djangocms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login
from os.path import stat
from rest_framework_jwt.views import obtain_jwt_token

from accounts.views import Index
from cms.urls import router as cms_router


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cms/', include('cms.urls', namespace='cms')),
    url(r'^api/', include(cms_router.urls)),
    url(r'^api-auth/', obtain_jwt_token),
    url(r'^accounts/login/$', login,
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout_then_login, name='logout'),
    url(r'^accounts/index/$', Index.as_view(), name='account_index'),
]
