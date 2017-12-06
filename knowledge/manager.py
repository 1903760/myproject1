from django.db import models


class ArticleManager(models.Manager):
    use_for_related_fields = True

    def article_status(self):
        return self.get_queryset().exclude(article_status=False)
