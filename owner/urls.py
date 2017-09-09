from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from owner import views 
 
app_name = 'owner'
 
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^mypage/$', views.mypage, name='mypage'),
    url(r'^redirect/$', views.redirect, name='redirect'),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'owner/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'owner/logout.html'},
        name='logout'
    ),
]
