from django.contrib.sitemaps import Sitemap
from django.urls import reverse  # Этот метод необходим, чтобы получить url из шаблона


class HomeSitemap(Sitemap):
    priority = 0.5  # Приоритет
    changefreq = 'daily'  # Частота проверки

    # Метод, возвращающий массив с url-ками
    def items(self):
        return ['home:index', 'home:contacts']

    # Метод непосредственной экстракции url из шаблона
    def location(self, item):
        return reverse(item)
