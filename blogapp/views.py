from django.views import View
from django.http import HttpResponse, HttpRequest
from django.urls import reverse_lazy
from django.contrib.syndication.views import Feed
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article


class HiBlogView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse('Hi Blog!')


class ArticlesListView(ListView):
    template_name = 'blogapp/articles-list.html'
    queryset = Article.objects.defer(
        'content'
        ).select_related(
            'author'
            ).select_related(
                'category'
                ).prefetch_related(
                    'tags'
                    ).all().order_by('-pub_date')
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    model = Article


class LatestArticleFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return (
            Article.objects.order_by('-created_at')[:5]
        )
    
    def item_title(self, item: Article) -> str:
        return item.title

    def item_description(self, item: Article) -> str:
        return item.content[0:200] + '...'