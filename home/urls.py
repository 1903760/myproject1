from django.conf.urls import url
from .views import *
from rss.views import *
from home.views import e_handler404, e_handler500


urlpatterns = [
    url(r'^$', EIndexView.as_view(), name='index'),
    # url(r'^feed/$', ArticlesFeed()),
]



handler404 = e_handler404
handler500 = e_handler500
