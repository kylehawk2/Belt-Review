from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^home/bookreview$', views.bookreview),
    url(r'^bookreview/add_book$', views.add_book),
    url(r'^book/(?P<id>\d+)$', views.book),
    url(r'user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
    url(r'^book/new_review$', views.new_review)
]