"""myproject URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views as sitemap_views      # Представление
from django.contrib.sitemaps import GenericSitemap              # Шаблонный класс для формирования страницы Sitemap
from django.views.decorators.cache import cache_page            # Декоратор кеширования
from knowledge import models as knowledge_models                # Модели статей и разделов, по которым будет формироваться Sitemap
from home.sitemap import HomeSitemap                            # Статический Sitemap для относительно постоянных страниц


# Объект карты разделов. Здесь просто забираются все объекты из базы данных,
# а также по одноимённому полю в модели забирается дата последней модификации
sitemap_sections = {
    'queryset': knowledge_models.Section.objects.all(),
    'date_field': 'section_lastmod',
}

# А вот со статьями уже интереснее. Здесь забираются только те статьи, которые опубликованы
# И для этого нужно будет написать специальный менеджер
sitemap_articles = {
    'queryset': knowledge_models.Article.objects.article_status(),
    'date_field': 'article_date',
}

# Формируем объект со всеми картами и присваиваем им наименования
sitemaps = {
    'sections': GenericSitemap(sitemap_sections, priority=0.5),
    'articles': GenericSitemap(sitemap_articles, priority=0.5),
    'home': HomeSitemap
}


urlpatterns = [
    url(r'^', include('home.urls', namespace='home')),
    url(r'^news/', include('knowledge.urls', namespace='news')),
    url(r'^admin/', admin.site.urls),
]


# Шаблоны URL, заметьте, здесь указано кеширование cache_page(86400)
# Первый шаблон будет формировать основную карту сайта, в которой будут указаны URL дочерних,
# То есть 'sitemap-sections', 'sitemap-articles', 'sitemap-home'
# Заметили, что их названия перекликаются с названиями параметров в объекте sitemaps?
urlpatterns += [
    url(r'^sitemap\.xml$', cache_page(86400)(sitemap_views.index), {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>\w+)\.xml$', cache_page(86400)(sitemap_views.sitemap), {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
]

