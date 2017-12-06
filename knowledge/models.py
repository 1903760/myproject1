from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from .manager import ArticleManager
from django.contrib.postgres.fields import ArrayField
# Create your models here.


class Section(models.Model):
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        db_table = 'section'

    section_title = models.CharField(verbose_name='Название', max_length=200)
    section_url = models.CharField(max_length=50, verbose_name='ссылка')
    section_description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return self.section_title

    def get_absolute_url(self):
        return reverse('news:section', kwargs={'section': self.section_url})


class Article(models.Model):
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        db_table = 'article'

    article_name = models.CharField('Название статьи', max_length=200)
    article_section = models.ForeignKey(Section, verbose_name='Раздел')
    article_user = models.ForeignKey(User, verbose_name='пользователь')
    article_date = models.DateField(verbose_name='Дата публикации', auto_now_add=True)
    article_content = models.TextField(verbose_name='Описание')
    article_status = models.IntegerField(verbose_name='Статус')
    objects = ArticleManager()          # объекты queryset подменяются менеджером для расширения функционала

    def __str__(self):
        return self.article_name

    def get_absolute_url(self):
        return reverse('news:article', kwargs={'section': self.article_section.section_url, 'article_id': self.id})


class Comment(models.Model):
    class Meta:
        db_table = 'comments'

    path = ArrayField(models.IntegerField())
    article_id = models.ForeignKey(Article)
    author_id = models.ForeignKey(User)
    content = models.TextField('Комментарий')
    pub_date = models.DateTimeField('Дата комментария')

    def __str__(self):
        return self.content[0:200]

    def get_offset(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return level

    def get_col(self):
        level = len(self.path) - 1
        if level > 5:
            level = 5
        return 12 - level
