from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from .models import *
from .forms import *
from django.contrib import auth
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.template.context_processors import csrf
# Create your views here.


class ENewsIndex(View):
    template_name = 'knowledge/index.html'

    def get(self, request, *args, **kwargs):
        context = {}
        context['section_list'] = Section.objects.all().order_by('section_title')
        return render(request, template_name=self.template_name, context=context)


class ESectionView(View):
    template_name = 'knowledge/section.html'

    def get(self, request, *args, **kwargs):
        context = {}
        section = get_object_or_404(Section, section_url=self.kwargs['section'])
        context['section'] = section
        return render(request, template_name=self.template_name, context=context)


class EArticleView(View):
    template_name = 'knowledge/article.html'
    comment_form = CommentForm

    def get(self, request,  *args, **kwargs):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        context = {}
        context.update(csrf(request))
        user = auth.get_user(request)
        context['article'] = article
        # Помещаем в контекст все комментарии, которые относятся к статье
        # попутно сортируя их по пути, ID автоинкрементируемые, поэтому
        # проблем с иерархией комментариев не должно возникать
        context['comments'] = article.comment_set.all().order_by('path')
        context['next'] = article.get_absolute_url()
        # Будем добавлять форму только в том случае, если пользователь авторизован
        if user.is_authenticated:
            context['form'] = self.comment_form

        return render(request, template_name=self.template_name, context=context)

    # Декораторы по которым, только авторизованный пользователь
    # может отправить комментарий и только с помощью POST запроса
    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        a = request.POST
        print(a)
        print(self.kwargs)
        form = CommentForm(self, request.POST)
        article = get_object_or_404(Article, id=self.kwargs['article_id'])

        if form.is_valid():
            comment = Comment()
            comment.path = []
            comment.article_id = article
            comment.author_id = auth.get_user(request)
            comment.content = form.cleaned_data['comment_area']
            print(comment)
            comment.save()

            # Django не позволяет увидеть ID комментария по мы не сохраним его,
            # хотя PostgreSQL имеет такие средства в своём арсенале, но пока не будем
            # работать с сырыми SQL запросами, поэтому сформируем path после первого сохранения
            # и пересохраним комментарий
            try:
                comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
                comment.path.append(comment.id)
                print('получилось')
            except ObjectDoesNotExist:
                comment.path.append(comment.id)
                print('не получилось')
            comment.save()
        return redirect('/')

