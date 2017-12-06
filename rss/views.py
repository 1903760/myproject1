from django.contrib.syndication.views import Feed
from django.shortcuts import render
from knowledge.models import Article

# Create your views here.


class ArticlesFeed(Feed):
    title = "Hitparad - Музыкальный портал"
    description = "Последние статьи сайта Hitparad"
    link = "/"

    def items(self):
        return Article.objects.exclude(article_status=False).order_by('-article_date')[:10]

    def item_title(self, item):
        return item.article_name

    def item_description(self, item):
        return item.article_content[0:400] + "<p>Статья впервые появилась на <a href='https://evileg.com/'> Hitparad.kz " \
                                             "- Музыкальный портал < / a > < / p > "

