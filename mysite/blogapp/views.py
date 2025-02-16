from keyword import kwlist

from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.views.generic import (
    ListView, DetailView,
)
from rest_framework.reverse import reverse_lazy

from .models import Article


class ArticleListView(ListView):
    template_name = 'blogapp/article_list.html'
    context_object_name = 'articles'

    queryset = (Article.objects.select_related('author', 'category')
                .prefetch_related('tags').defer('author__bio'))

class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy('blogapp:articles_list')

    def items(self):
        return (Article.objects.filter(pub_date__isnull=False)
                .order_by('-pub_date')[:5])

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]
