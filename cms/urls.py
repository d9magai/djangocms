from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rest_framework import routers

from cms import views

from .views import BookViewSet, ImpressionViewSet


urlpatterns = [
    url(r'^redirect/$', views.redirect, name='redirect'),
    url(r'^index$', views.index, name='index'),
    url(
        r'^login/$',
        auth_views.login,
        {'template_name': 'cms/login.html'},
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'template_name': 'cms/logout.html'},
        name='logout'
    ),
    # 書籍
    url(r'^book/$', views.BookList.as_view(), name='book_list'),   # 一覧
    url(r'^book/add/$', views.book_edit, name='book_add'),  # 登録
    url(r'^book/mod/(?P<book_id>\d+)/$', views.book_edit, name='book_mod'),  # 修正
    url(r'^book/del/(?P<book_id>\d+)/$', views.book_del, name='book_del'),   # 削除
    # 感想
    url(r'^impression/(?P<book_id>\d+)/$',
        views.ImpressionList.as_view(), name='impression_list'),  # 一覧
    url(r'^impression/add/(?P<book_id>\d+)/$',
        views.impression_edit, name='impression_add'),        # 登録
    url(r'^impression/mod/(?P<book_id>\d+)/(?P<impression_id>\d+)/$',
        views.impression_edit, name='impression_mod'),  # 修正
    url(r'^impression/del/(?P<book_id>\d+)/(?P<impression_id>\d+)/$',
        views.impression_del, name='impression_del'),   # 削除
]


router = routers.DefaultRouter()
router.register(r'book', BookViewSet)
router.register(r'imporession', ImpressionViewSet)
