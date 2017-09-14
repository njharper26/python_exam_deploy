from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/register$', views.process_register),
    url(r'^process/login$', views.process_login),
    url(r'^logout$', views.logout),    
    url(r'^success$', views.success),    
    url(r'^quotes$', views.quotes_dashboard),
    url(r'^proccess/add$', views.proccess_add_quote),
    url(r'^proccess/favorite/(?P<id>\d+)$', views.proccess_add_favorite),
    url(r'^proccess/remove/(?P<id>\d+)$', views.proccess_remove_favorite),
    url(r'^user/(?P<id>\d+)$', views.user_profile)
]

    # url(r'^books$', views.show),
    # url(r'^books/add$', views.add),
    # url(r'^process/add$', views.process_add_book_review),
    # url(r'^process/review/(?P<id>\d+)$', views.process_review),
    # url(r'^books/(?P<id>\d+)$', views.book),
    # url(r'^user/(?P<id>\d+)$', views.user)