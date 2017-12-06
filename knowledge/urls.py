from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', ENewsIndex.as_view(), name='index'),
    url(r'^(?P<section>[\w]+)/$', ESectionView.as_view(), name='section'),
    url(r'^(?P<section>[\w]+)/(?P<article_id>[0-9]+)/$', EArticleView.as_view(), name='article'),
    # url(r'^comment/(?P<article_id>[0-9]+)/$', EArticleView.post, name='add_comment'),
]
